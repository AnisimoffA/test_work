### Решение без добавления новой таблицы:

```python
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name LIKE short_names.name || '%'
  AND short_names.status IS NOT NULL;
```
___

### Решение с добавлением новой таблицы:

```python
CREATE TEMPORARY TABLE new_table AS
SELECT f.id, s.status
FROM full_names f
JOIN short_names s ON f.name LIKE s.name || '%'
WHERE s.status IS NOT NULL;

UPDATE full_names
SET status = new_table.status
FROM new_table
WHERE full_names.id = new_table.id;
```
___

### Решение с добавлением индексов:

```python
CREATE INDEX idx_short_names_name ON short_names(name);
CREATE INDEX idx_full_names_name ON full_names(name);

UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name LIKE CONCAT(short_names.name, '%')
  AND short_names.status IS NOT NULL;
```