## Проверка работоспособности системы

### 1. Проверка корректности ввода данных:
   - Проверка на пустые поля. Если одно из полей (широта или долгота для начальной или конечной точки маршрута) не заполнено, система выводит сообщение о необходимости заполнения всех полей.
   - Проверка на корректность введённых координат. Ввод координат вне допустимых диапазонов (широта от -90 до 90, долгота от -180 до 180) вызывает ошибку и соответствующее сообщение о неверных данных.
   
   **Пример ошибки**:  
   _"Проверьте корректность координат и повторите попытку."_

### 2. Проверка подключения к интернету:
   - Приложение проверяет наличие активного интернет-соединения перед выполнением запроса к API. Если сеть отсутствует, пользователю выводится сообщение с предложением проверить подключение.

   **Пример ошибки**:  
   _"Ошибка подключения: проверьте ваше интернет-соединение."_

### 3. Проверка доступности API:
   - Приложение пытается получить данные о погоде через внешнее API. В случае недоступности API или возникновения сетевых ошибок пользователю будет выведено сообщение с подробным описанием проблемы.

   **Пример ошибки**:  
   _"Ошибка подключения к серверу. Проверьте ваше интернет-соединение."_

### 4. Проверка корректности получения данных о погоде:
   - После того как данные о погоде получены, приложение проверяет наличие ошибок в ответах API. Если для какой-либо из точек маршрута данные не могут быть получены, пользователю будет выведено соответствующее сообщение.

   **Пример ошибки**:  
   _"Ошибка при получении данных о погоде для начальной точки, попробуйте ввести корректные координаты ещё раз."_

### 5. Тестирование:
   - Ввод корректных координат для начальной и конечной точек.
   - Ввод некорректных координат, выходящие за рамки установленных ограничений.
   - Проверка работы приложения при отключённом интернет-соединении.
   - Проверка работы приложения при недоступности API или других ошибок сервера.

Приложение понятно информирует пользователя о возникших проблемах.
