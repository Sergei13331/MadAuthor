# MadAuthor
3D игра написанная на python с использованием pygame.

### Геймплей
В игре задача игрока вовремя нажать на пробел, пока новый появившийся квадрат не стал слишком красный. Также нельзя
нажимать пробел пока квадрат ещё зелёный.
Камера постоянно вращается вокруг поля с рандомными скоростью и направлением. Расположение квадратов также полностью рандомно (в пределах поля видимости).

### Структура кода
Реализован классы графики (Engine), объекта (GameObject) и камеры (Camera).
Главный цикл, в котором отрисовывается графика, расположен в классе графики.
Цикл проходится по списку объектов и производит преобразование положения вершин из экземпряра объекта (пространство объекта)
в координаты камеры (пространство камеры), что позволяет отрисовывать 3D изображение в pygame.
Оперируя простыми преобразованиями, получилось сделать игру.
