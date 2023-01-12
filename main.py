import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Построить нечеткую базу знаний (использовать не менее 3 лингвистических переменных) для задачи определения
# временных затрат для выдачи заказа в ПБО (учитывая индивидуальную скорость работы сотрудников, количество
# посетителей,техническое состояние техники),проверить ее на полноту и произвести нечеткий вывод для конкретных
# значений (выбрать случайным образом).
def main():
    # переменные для задачи - заказ в ПБО (скорость работы сотрудников(в секундах, минимум 30 сек. максимум 100),
    # количество посетителей(максимум 50 человек),
    # техническое состояние техники(0-не работает, 10- работает без сбоев),
    # итоговое время обслуживания).
    condition = ctrl.Antecedent(np.arange(0, 10, 1), 'condition')
    amount = ctrl.Antecedent(np.arange(0, 50, 1), 'amount')
    speed = ctrl.Antecedent(np.arange(30, 100, 1), 'speed')
    time = ctrl.Consequent(np.arange(60, 200), 'time')

    # используем стандартную функцию принадлежности (треугольник)
    time.automf(names=['low', 'medium', 'high'])

    condition['low'] = fuzz.trapmf(condition.universe, [0, 1, 3, 5])
    condition['high'] = fuzz.trapmf(condition.universe, [4, 6, 8, 10])

    amount['low'] = fuzz.trapmf(amount.universe, [0, 1, 3, 7])
    amount['medium'] = fuzz.trapmf(amount.universe, [6, 11, 16, 20])
    amount['high'] = fuzz.trapmf(amount.universe, [16, 33, 45, 50])

    speed['low'] = fuzz.trapmf(speed.universe, [30, 33, 45, 50])
    speed['medium'] = fuzz.trapmf(speed.universe, [49, 52, 57, 66])
    speed['high'] = fuzz.trapmf(speed.universe, [65, 87, 95, 100])

    condition.view()
    amount.view()
    speed.view()
    time.view()

    # база правил
    rule1 = ctrl.Rule(condition['low'] & amount['low'] & speed['low'], time['low'])
    rule2 = ctrl.Rule(condition['high'] & amount['high'] & speed['high'], time['high'])
    rule3 = ctrl.Rule(condition['low'] & amount['low'] & speed['medium'], time['medium'])
    rule4 = ctrl.Rule(condition['low'] & amount['low'] & speed['high'], time['high'])
    rule5 = ctrl.Rule(condition['low'] & amount['medium'] & speed['low'], time['medium'])
    rule6 = ctrl.Rule(condition['low'] & amount['high'] & speed['low'], time['medium'])
    rule7 = ctrl.Rule(condition['high'] & amount['low'] & speed['low'], time['low'])
    rule8 = ctrl.Rule(condition['low'] & amount['medium'] & speed['medium'], time['medium'])
    rule9 = ctrl.Rule(condition['low'] & amount['medium'] & speed['high'], time['high'])
    rule10 = ctrl.Rule(condition['high'] & amount['medium'] & speed['low'], time['low'])
    rule11 = ctrl.Rule(condition['high'] & amount['medium'] & speed['medium'], time['medium'])
    rule12 = ctrl.Rule(condition['high'] & amount['medium'] & speed['high'], time['high'])
    rule13 = ctrl.Rule(condition['low'] & amount['high'] & speed['medium'], time['high'])
    rule14 = ctrl.Rule(condition['high'] & amount['low'] & speed['medium'], time['low'])
    rule15 = ctrl.Rule(condition['high'] & amount['high'] & speed['medium'], time['medium'])
    rule16 = ctrl.Rule(condition['low'] & amount['high'] & speed['high'], time['high'])
    rule17 = ctrl.Rule(condition['high'] & amount['low'] & speed['high'], time['medium'])
    rule18 = ctrl.Rule(condition['high'] & amount['high'] & speed['low'], time['low'])

    time_ctrl = ctrl.ControlSystem(
        [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
         rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18])
    time_simulator = ctrl.ControlSystemSimulation(time_ctrl)

    time_simulator.input['condition'] = 1
    time_simulator.input['amount'] = 10
    time_simulator.input['speed'] = 31
    time_simulator.compute()
    print(time_simulator.output['time'])  # 129.50000000000017

    condition.view(sim=time_simulator)
    amount.view(sim=time_simulator)
    speed.view(sim=time_simulator)
    time.view(sim=time_simulator)
    plt.show()


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    main()
