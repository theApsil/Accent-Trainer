# Пайплайн анализа произношения

Документ описывает путь данных от записи речи до выдачи советов.
```bash
[User audio] → [Preprocess] → [ASR + Align] → [Per-phoneme features] →
[Compare with reference] → [Generate advice + viz] → [Persist Attempt]
```
---

## 1. Запись и предобработка

Frontend:
- MediaRecorder пишет в audio/webm (Opus) с sampleRate=48000.
- Перед отправкой нормализуется громкость (`wavesurfer.js` peak normalization).
- POST /api/v1/attempts (multipart/form-data + JSON метаданные).

Backend:
- Сохранение исходника в MinIO bucket user-recordings.
- Конвертация в WAV mono 16 kHz, PCM16 через ffmpeg (Whisper и Praat ожидают именно это).
- Триммирование тишины (librosa `effects.trim`).

---

## 2. ASR + Forced Alignment

Инструмент: faster-whisper (модель base или small для скорости,
medium для качества; язык фиксируем `en`).

Шаги:
1. Транскрипция → текст с word-level timestamps.
2. Сравнение с эталонным текстом упражнения (Levenshtein / WER).
3. Forced alignment:
   - вариант A: whisperx (надстройка с wav2vec2 для точных фонемных границ);
   - вариант B: фонемизация эталона через g2p_en (ARPAbet) и сопоставление
     по словам через whisper word_timestamps=True.
4. Результат: список [(phoneme, start_ms, end_ms), ...].

---

## 3. Извлечение признаков на фонему

Для каждого временного интервала фонемы:

### MFCC
- librosa.feature.mfcc: n_mfcc=13, hop=10ms, win=25ms.
- Усреднение по фонеме → вектор 13.

### Форманты (только для гласных и сонорных)
- parselmouth (Burg method): F1, F2, F3 в Hz.
- Усреднение по стабильному центру фонемы (берём средние 60%).

### Спектрограмма
- Mel-спектрограмма для всего слова (для визуализации).
- Сохраняется как PNG в MinIO bucket spectrograms или возвращается как
  base64 (для коротких).

---

## 4. Сравнение с эталоном

Источник эталонов:
- Hillenbrand et al. (1995) — F1/F2/F3 по полу/возрасту для всех гласных
  American English. CSV в backend/data/hillenbrand_vowels.csv.
- Для согласных — спектральный центроид и шумовые полосы (предзаписанные
  статистики).

Алгоритм:
```python
for phoneme in attempt.phonemes:
    if phoneme.is_vowel:
        ref = hillenbrand[phoneme.symbol][user.demographic]
        dF1 = user.F1 - ref.F1
        dF2 = user.F2 - ref.F2
        # → отклонение в плоскости F1/F2
    else:
        # сравнение по MFCC косинусным расстоянием
        sim = cosine(user.mfcc, ref.mfcc_centroid)
```
Каждая фонема получает score 0..1 и тип ошибки (low_tongue,
high_tongue, too_front, too_back, no_voicing, …).

---

## 5. Маппинг формант → положение языка

Классическая интерпретация:

| Признак | Связь |
|---|---|
| F1 ↑ | язык ниже (открытая гласная) |
| F1 ↓ | язык выше (закрытая гласная) |
| F2 ↑ | язык более передний |
| F2 ↓ | язык более задний |

Нормализуем:
height    = normalize(F1, F1_min, F1_max)   # 0 = high, 1 = low
frontness = normalize(F2, F2_min, F2_max)   # 0 = back, 1 = front
→ TonguePosition(height, frontness) отдаётся фронту, SVG-схема языка
отрисовывает позицию пользователя и эталона рядом.

---

## 6. Генерация советов

Простые правила (`infrastructure/audio/advice_generator.py`):
if dF1 > THRESHOLD:  "опустите язык, шире раскройте рот"
if dF1 < -THRESHOLD: "поднимите язык ближе к нёбу"
if dF2 > THRESHOLD:  "сместите язык назад"
if dF2 < -THRESHOLD: "продвиньте язык вперёд"
Шаблоны фраз — на двух уровнях:
- техническое (для студию фонетики): «F1 завышен на 120 Hz»;
- бытовое (для пользователя): «попробуйте опустить челюсть ниже».

Каждый совет сопровождается визуальным маркером на TongueDiagram.

---

## 7. Сохранение и прогресс

- Создаётся Attempt с агрегированным score.
- Если score >= passing_threshold (например, 0.8) — Task помечается как
  пройденный.
- Progress модуля пересчитывается = % пройденных задач.
- При progress == 100% пользователю предлагается Final Check —
  одно предложение, содержащее все целевые фонемы модуля.

---

## 8. Эталонное произношение (всегда доступно)

Для каждой Task хранится URL в MinIO bucket reference-audio:
- При первом обращении: проверяем кэш → если нет, Piper TTS генерирует
  WAV и кладёт в MinIO.
- Для частотных слов — предгенерация через seed-скрипт.
- Опционально подмешиваются сэмплы CMU ARCTIC (натуральный голос).

Frontend получает pre-signed URL и проигрывает <audio>.