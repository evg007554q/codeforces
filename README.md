Парссинг задач с сайта https://codeforces.com/

Приложение загружает задачи базу данных postgres.
Пользователь взаимодействует с приложением через telegram — Bot

Работа с ботом.

1.Выберете сложность

![изображение](https://github.com/evg007554q/codeforces/assets/131668392/eb83594b-4802-4173-876c-347320ee26de)


2. Выберете категию/тему/
![изображение](https://github.com/evg007554q/codeforces/assets/131668392/65914a53-f281-4bdc-8ef9-2be7b272aeb2)

для поиска используйте кнопки навигации «Вперед» «Назад» или введите текст для поиска.
![изображение](https://github.com/evg007554q/codeforces/assets/131668392/60319a3d-61ac-4480-a510-7a987408ae05)


4. После выбора категории выпадает список задач порциями по 10 шт по выбраной сложности и категории.
![изображение](https://github.com/evg007554q/codeforces/assets/131668392/d3c04903-aa79-4a47-afbd-413e3659b6bf)

для просмотра списка задач используте кнопки «Вперед» «Назад». 
![изображение](https://github.com/evg007554q/codeforces/assets/131668392/cabf077f-fb13-41c8-adc3-5dae8bae6e98)

Для поиска конкретной задачи нажмите «Уточнить поиск» или введите строку поиска
![изображение](https://github.com/evg007554q/codeforces/assets/131668392/afbb99ae-bbdb-426d-9c3b-ce8b95e72d69)


Настройка приложения.
1. Клонировать проект  
git clone https://github.com/evg007554q/codeforces

2. Создать виртуальное окружение, установить библиотеки
pip install - r  requirements.txt

3. Создайть БД  postgres скрипт Create.sql.

4. Регистрация бота в BotFather.

5. Создайте файл с переменными окружения в файле .env. Пример файла .env.sample

