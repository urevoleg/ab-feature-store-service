# Trigger Engine for AB-feature store

Trigger Engine — это Python-сервис для обработки событий мобильного приложения
и вычисления пользовательских флагов и метрик на основе YAML-описанных триггеров.

Сервис читает события из Kafka, декодирует `binaryData`, извлекает события,
применяет правила (триггеры) и накапливает состояние пользователей
(флаги и счётчики).

---

## Основные возможности

- Чтение событий из Kafka (`event-stream-v1`)
- Поддержка нескольких событий внутри одного сообщения
- YAML-конфигурация триггеров (без изменения кода)
- Два типа триггеров:
  - **flag** — срабатывает один раз в день на пользователя
  - **metric** — считает количество событий
- Простой DSL для фильтрации событий (`=`, `in`, `and`, `or`)
- Расширенный DSL для event_name (`in`, `eq`, `regex`)
- InMemory state store (для локальной разработки)
- Готовность к расширению (Redis, S3, Iceberg)

---


## Архитектура

```text
Kafka (event-stream-v1)
        │
        ▼
┌────────────────────┐
│ Kafka Consumer     │
│ (kafka-python)     │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Binary Decoder     │
│ base64 → JSON      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Event Extractor    │
│ event_prop[]       │
│ magnit_id          │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Trigger Engine     │
│ YAML + DSL         │
│ flag / metric      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ State Store        │
│ InMemory (per day) │
└────────────────────┘
```

## Пример конфигурации триггеров

```yaml
triggers:
  - name: add_to_cart_counts
    description: Добавление в корзину
    type: metric
    event_name: 
      eq: add_to_cart
    where:
      in:
        action: [add_to_cart]

  - name: favCategory_flag
    description: Просмотр любимых категорий
    type: flag
    event_name:
      regex: '.*'
    where:
      eq:
        page: favCategory
```

Выходной результат Store (результат может быть сохранен в БД):

```json
{
  '2026-02-06': {
    '014dfea7-f697-4683-be8b-346d712198a0': {
      'flags': {
        'app_launch_flag',
        'favCategory_flag'
      },
      'metrics': {
        'click_counts': 4
      }
    },
    '69fc4284-81a5-4a31-9650-609f35a89eef': {
      'flags': {
        'app_launch_flag',
        'favCategory_flag',
        'mainpage_click_flag'
      },
      'metrics': {
        'add_to_cart_counts': 2,
        'click_counts': 8
      }
    }
  }
}

```

### Как интерпретировать результат

Пользователь `014dfea7-f697-4683-be8b-346d712198a0`:
* ✅ Запускал приложение (app_launch_flag)
* ✅ Кликал на избранную категорию (favCategory_flag)
* 🔢 Совершил 4 клика (click_counts = 4)
* ❌ Не добавлял товары в корзину

Пользователь `69fc4284-81a5-4a31-9650-609f35a89eef`:
* ✅ Запускал приложение
* ✅ Кликал на избранную категорию
* ✅ Кликал на главный экран
* 🔢 8 кликов по главной странице
* 🛒 2 добавления в корзину