-- 1. Отримати всі завдання певного користувача
SELECT * FROM tasks WHERE user_id = 10

-- 2. Вибрати завдання за певним статусом
SELECT * FROM tasks WHERE status_id = (SELECT id FROM statuses WHERE name = 'new')

-- 3. Оновити статус конкретного завдання
UPDATE tasks SET status_id = (SELECT id FROM statuses WHERE name = 'in progress') WHERE id = 1

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'Description', 1, 2)

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks WHERE status_id != (SELECT id FROM statuses WHERE name = 'completed')

-- 7. Видалити конкретне завдання
DELETE FROM tasks WHERE id = 1

-- 8. Знайти користувачів з певною електронною поштою
SELECT * FROM users WHERE email LIKE '%@example.net'

-- 9. Оновити ім'я користувача
UPDATE users SET fullname = 'Updated Name' WHERE id = 1

-- 10. Отримати кількість завдань для кожного статусу
  SELECT s."name"
       , COUNT(*)
    FROM tasks t
    JOIN statuses s
      ON s.id = t.status_id
GROUP BY s."name"

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
SELECT t.title
     , u.email
  from tasks t
  join users u
    on t.user_id = u.id
   and email LIKE '%@example.net'

-- 12. Отримати завдання, що не мають опису
SELECT * FROM tasks WHERE description IS null or description = ''

-- 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
    SELECT u.fullname
         , t.title
      FROM users u
INNER JOIN tasks t
        ON u.id = t.user_id
INNER JOIN statuses s
        ON s.id = t.status_id
       and s.name = 'in progress'

-- 14. Отримати користувачів та кількість їхніх завдань
   SELECT u.fullname
        , COUNT(t.id)
     FROM users u
LEFT JOIN tasks t
       ON u.id = t.user_id
 GROUP BY u.id
