
---

# Простой DSL для фильтрации событий

## Цель DSL

- Проверять **event_attrs**
- Поддержать:
  - `eq` — равно
  - `in` — вхождение в массив
  - `and`, `or`

---

## DSL в YAML

### Примеры

### Конкретное событие (может быть без where)

```yaml
event_name: 
  eq: todayMain
```

### Проверка списка

```yaml
event_name:
  in:
    - event_name_1
    - event_name_2
```

### Регулярки, start/ends_with

```yaml
event_name:
  regex: "^delivery_.*_view$"
```
------------------------
```yaml
event_name:
  or:
    - ends_with: "_favCategory_success_view"
    - ends_with: "_favCategoryTiles_success_view"
```


### Простое равенство
```yaml
where:
  eq:
    action: view
```

### Вхождение в массив

```yaml
where:
  in:
    page: [catalogScreen, productCard]
```

### AND

```yaml
where:
  and:
    - eq:
        action: click
    - in:
        block: [mainpage, catalog]
```


### OR

```yaml
where:
  or:
    - eq:
        page: catalog
    - eq:
        page: search

```