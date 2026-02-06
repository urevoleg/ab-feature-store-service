
---

# Простой DSL для фильтрации событий

## Цель DSL

- Проверять **event_attrs**
- Поддержать:
  - `eq` — равно
  - `in` — вхождение в массив
  - `and`, `or`
- Без `eval`, безопасно и прозрачно

---

## DSL в YAML

### Примеры

### 1. Простое равенство
```yaml
where:
  eq:
    action: view
```

## Вхождение в массив

```yaml
where:
  in:
    page: [catalogScreen, productCard]
```

## AND

```yaml
where:
  and:
    - eq:
        action: click
    - in:
        block: [mainpage, catalog]
```


## OR

```yaml
where:
  or:
    - eq:
        page: catalog
    - eq:
        page: search

```