from solution import read_csv_data, generate_report, save_json_report


def main():
    input_file = 'pumps_data.csv'
    output_file = 'pump_report.json'

    print("=" * 50)
    print("ИМИТАЦИЯ РАБОТЫ ДИСПЕТЧЕРА НПС")
    print("=" * 50)

    print(f"\n[1/3] Чтение данных из {input_file}...")
    try:
        data = read_csv_data(input_file)
        print(f"      ✓ Успешно прочитано {len(data)} записей")
    except FileNotFoundError:
        print(f"      ✗ Ошибка: файл {input_file} не найден!")
        return
    except Exception as e:
        print(f"      ✗ Ошибка при чтении: {e}")
        return

    print(f"\n[2/3] Генерация отчёта...")
    try:
        report = generate_report(data)
        print("      ✓ Отчёт успешно сгенерирован")
    except Exception as e:
        print(f"      ✗ Ошибка при генерации отчёта: {e}")
        return

    print(f"\n[3/3] Сохранение отчёта в {output_file}...")
    try:
        save_json_report(report, output_file)
        print("      ✓ Отчёт сохранён")
    except Exception as e:
        print(f"      ✗ Ошибка при сохранении: {e}")
        return

    print("\n" + "=" * 50)
    print("СВОДКА ПО ОТЧЁТУ")
    print("=" * 50)
    print(f"Количество насосов:        {report['report_info']['total_pumps']}")
    print(f"Количество сессий:         {report['report_info']['total_sessions']}")
    print(f"Общее время работы:        {report['summary']['total_operating_time_hours']} ч")
    print(f"Общий объём:               {report['summary']['total_pumped_volume_m3']} м³")
    print(f"Средний расход:            {report['summary']['average_flow_rate_m3h']} м³/ч")
    print("=" * 50)
    print(f"\n✓ Работа завершена! Отчёт сохранён в {output_file}")


if __name__ == "__main__":
    main()