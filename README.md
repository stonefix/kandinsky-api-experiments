# kandinsky-api-experiments
Repository with experiments and results

В рамках ограниченного кол-ва времени и увлеченностью над экспериментами, 
мы не заворачивали в докерфайлы прототип бэкенда на FastAPI и прочие штуки, 
а приложили, то что точно работало.

Для работы со скриптами необходимо создать `.env` файл для переменных окружения:
`URL=https://api-key.fusionbrain.ai/`
а  также с `API_KEY` и `SECRET_KEY` 
для `API Kandinsky`

В репозитории следующее:


`api.py` - Скрипт для запроса к API Kandinsky, получения промпта по тексту 'Dark Side Stop For Stop all this'
(заданному в переменной TEXT в 70-й строке этого скрипта)
А также генерации QR-а по этому же тексту.

`generator_checker_qr_script.py` - Данный скрипт реализует генерацию QR-кодов по словам/ссылкам/словосочетаниям из датасета dataset.csv

Полученная картинка из Kandinsky накладывается, как маска в наш полученный QR-код.
- Это самый брутфорсный и банальный вариант.
- Ещё добавится выделение границ QR-кода для его постоянного чтения, независимо от маски

`utils.py` - Вспомогательные утилиты для Base64 to Image, для Base64 to Buffer, для генерации QR-кодов и т.п. 

`Копия_блокнота__Control_nt1_ipynb_.ipynb` - jupyter notebook, в котором мы проводили эксперименты и добились корректных QR-кодов. (Дообучение в рамках хакатона не доделали)
