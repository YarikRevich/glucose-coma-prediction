import csv
import random
import sys

HOURS = 24 * 30 * 6
MEASUREMENTS_PER_HOUR = 60

WARNING_SLOPE_THRESHOLD = -15
COMA_SLOPE_THRESHOLD = -25

CRITICAL_DROP_PROB = 0.0003
CRITICAL_SPIKE_PROB = 0.0001
EXTREME_START_PROB = 0.02

COMA_LOW_PROB = 0.0003
COMA_HIGH_PROB = 0.0002

def main(output: str) -> None:
    if random.random() < EXTREME_START_PROB:
        glucose = random.choice([
            random.randint(30, 44),    
            random.randint(601, 650) 
        ])
    else:
        glucose = random.randint(90, 130)

    data = []
    previous_slope = 0
    hour_block = []

    for hour in range(HOURS):
        if hour_block:
            glucose_values = [item['glucose'] for item in hour_block]
            slopes = [item['slope'] for item in hour_block]
            accelerations = [item['acceleration'] for item in hour_block]

            label = "0"
            if any(g < 45 or g > 600 for g in glucose_values):
                label = "1"
            elif any(s <= COMA_SLOPE_THRESHOLD or (s <= WARNING_SLOPE_THRESHOLD and a <= -10)
                     for s, a in zip(slopes, accelerations)):
                label = "1"

            data.append({
                "glucose_values": glucose_values,
                "label": label
            })

        hour_block = []

        for measure in range(MEASUREMENTS_PER_HOUR):
            delta = random.randint(-10, 10)

            hour_of_day = hour % 24
            if 6 <= hour_of_day <= 8:
                delta += random.randint(5, 15)
            elif 12 <= hour_of_day <= 13:
                delta += random.randint(5, 15)
            elif 18 <= hour_of_day <= 20:
                delta += random.randint(5, 15)
            elif 2 <= hour_of_day <= 5:
                delta += random.randint(-15, -5)

            chance = random.random()
            if chance < COMA_LOW_PROB:
                new_glucose = random.randint(20, 44)
            elif chance < COMA_LOW_PROB + COMA_HIGH_PROB:
                new_glucose = random.randint(601, 650)
            elif chance < COMA_LOW_PROB + COMA_HIGH_PROB + CRITICAL_DROP_PROB:
                delta = random.randint(-80, -50)
                new_glucose = glucose + delta
            elif chance < COMA_LOW_PROB + COMA_HIGH_PROB + CRITICAL_DROP_PROB + CRITICAL_SPIKE_PROB:
                delta = random.randint(50, 100)
                new_glucose = glucose + delta
            else:
                new_glucose = glucose + delta

            if chance >= COMA_LOW_PROB + COMA_HIGH_PROB:
                if new_glucose < 40:
                    new_glucose = 40 + random.randint(0, 10)
                elif new_glucose > 650:
                    new_glucose = 650 - random.randint(0, 20)

            if hour == 0 and measure == 0:
                slope = 0
                acceleration = 0
            else:
                slope = new_glucose - glucose
                acceleration = slope - previous_slope

            hour_block.append({
                "glucose": new_glucose,
                "slope": slope,
                "acceleration": acceleration
            })

            previous_slope = slope
            glucose = new_glucose

    if hour_block:
        glucose_values = [item['glucose'] for item in hour_block]
        slopes = [item['slope'] for item in hour_block]
        accelerations = [item['acceleration'] for item in hour_block]

        label = "0"
        if any(g < 45 or g > 600 for g in glucose_values):
            label = "1"
        elif any(s <= COMA_SLOPE_THRESHOLD or (s <= WARNING_SLOPE_THRESHOLD and a <= -10)
                 for s, a in zip(slopes, accelerations)):
            label = "1"

        data.append({
            "glucose_values": glucose_values,
            "label": label
        })

    for i in range(len(data) - 1):
        data[i]["future_label"] = data[i + 1]["label"]
    data = data[:-1] 

    fieldnames = [f"glucose_{i}" for i in range(1, MEASUREMENTS_PER_HOUR + 1)] + ["future_label"]

    with open(output, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            flat_row = {"future_label": row["future_label"]}
            flat_row.update({f"glucose_{i+1}": row["glucose_values"][i] for i in range(MEASUREMENTS_PER_HOUR)})
            writer.writerow(flat_row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Not enough arguments provided!")
    
    main(sys.argv[1])
