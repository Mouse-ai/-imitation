import csv
import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any


def parse_time(time_str: str) -> datetime:
    """Parse time string in various formats"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%d.%m.%Y %H:%M:%S",
        "%H:%M:%S",
        "%H:%M"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse time: {time_str}")


def calculate_duration_hours(start_time: str, stop_time: str) -> float:
    """Calculate duration in hours between two timestamps"""
    start = parse_time(start_time)
    stop = parse_time(stop_time)

    # If stop time is before start time, assume it's next day
    if stop < start:
        stop = stop.replace(day=stop.day + 1)

    duration = (stop - start).total_seconds() / 3600  # Convert to hours
    return round(duration, 4)


def read_csv_data(filename: str) -> List[Dict[str, Any]]:
    """Read pump data from CSV file"""
    data = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pump_id = row['pump_id'].strip()
            start_time = row['start_time'].strip()
            stop_time = row['stop_time'].strip()
            flow_rate = float(row['flow_rate_m3h'].strip())

            duration = calculate_duration_hours(start_time, stop_time)
            volume = round(flow_rate * duration, 4)

            data.append({
                'pump_id': pump_id,
                'start_time': start_time,
                'stop_time': stop_time,
                'flow_rate_m3h': flow_rate,
                'duration_hours': duration,
                'volume_m3': volume
            })

    return data


def generate_report(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate JSON report from pump data"""

    # Calculate statistics per pump
    pump_stats = defaultdict(lambda: {
        'total_duration_hours': 0,
        'total_volume_m3': 0,
        'sessions': []
    })

    for record in data:
        pump_id = record['pump_id']
        pump_stats[pump_id]['total_duration_hours'] += record['duration_hours']
        pump_stats[pump_id]['total_volume_m3'] += record['volume_m3']
        pump_stats[pump_id]['sessions'].append({
            'start_time': record['start_time'],
            'stop_time': record['stop_time'],
            'duration_hours': record['duration_hours'],
            'volume_m3': record['volume_m3']
        })

    # Round values
    for pump_id in pump_stats:
        pump_stats[pump_id]['total_duration_hours'] = round(
            pump_stats[pump_id]['total_duration_hours'], 4
        )
        pump_stats[pump_id]['total_volume_m3'] = round(
            pump_stats[pump_id]['total_volume_m3'], 4
        )

    # Calculate total statistics
    total_duration = sum(record['duration_hours'] for record in data)
    total_volume = sum(record['volume_m3'] for record in data)

    # Build report
    report = {
        'report_info': {
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_pumps': len(pump_stats),
            'total_sessions': len(data)
        },
        'summary': {
            'total_operating_time_hours': round(total_duration, 4),
            'total_pumped_volume_m3': round(total_volume, 4),
            'average_flow_rate_m3h': round(total_volume / total_duration, 4) if total_duration > 0 else 0
        },
        'pumps': dict(pump_stats)
    }

    return report


def save_json_report(report: Dict[str, Any], filename: str) -> None:
    """Save report to JSON file"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(report, file, ensure_ascii=False, indent=2)