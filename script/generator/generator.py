import csv
import random
import uuid
from typing import List, Dict, Tuple

__all__ = ["generate"]

MEASUREMENTS_PER_HOUR = 60

WARNING_SLOPE_THRESHOLD = -15
COMA_SLOPE_THRESHOLD = -25
HYPOGLYCEMIA_THRESHOLD = 60  
HYPERGLYCEMIA_THRESHOLD = 250 
SEVERE_HYPOGLYCEMIA_THRESHOLD = 45
SEVERE_HYPERGLYCEMIA_THRESHOLD = 400

PATIENT_COUNT = 100  
MIN_DAYS = 10  

CRITICAL_DROP_PROB = 0.0005  
CRITICAL_SPIKE_PROB = 0.0005 
SEVERE_EVENT_PROB = 0.001  

class PatientProfile:
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        
        self.baseline_glucose = random.randint(80, 140)
        self.glucose_volatility = random.uniform(0.5, 2.0)
        
        self.meal_response = random.uniform(0.5, 2.0)
        self.meal_delay = random.randint(10, 30)
        
        self.activity_response = random.uniform(0.5, 2.0)
        
        self.dawn_effect = random.uniform(0, 2.0)
        self.nocturnal_drop = random.uniform(0, 1.5)
        
        self.hypo_risk = random.uniform(0.1, 1.5)
        self.hyper_risk = random.uniform(0.1, 1.5)
        
        self.recovery_rate = random.uniform(0.1, 0.5)

def generate_meal_schedule() -> List[Tuple[int, int]]:
    """Generate a day's meal schedule with some variability"""
    
    meals = []
    
    breakfast_hour = random.randint(5, 9)
    breakfast_minute = random.randint(0, 59)
    meals.append((breakfast_hour, breakfast_minute))
    
    lunch_hour = random.randint(11, 14)
    lunch_minute = random.randint(0, 59)
    meals.append((lunch_hour, lunch_minute))
    
    dinner_hour = random.randint(17, 20)
    dinner_minute = random.randint(0, 59)
    meals.append((dinner_hour, dinner_minute))
    
    if random.random() < 0.5:
        snack_hour = random.choice([10, 15, 22])
        snack_minute = random.randint(0, 59)
        meals.append((snack_hour, snack_minute))
    
    return meals

def generate_activity_schedule() -> List[Tuple[int, int, int]]:
    """Generate a day's physical activity schedule - (hour, minute, duration_minutes)"""
    
    activities = []
    
    if random.random() < 0.7:
        activity_hour = random.choice([7, 12, 18])
        activity_minute = random.randint(0, 59)
        duration = random.randint(15, 60)  # 15 minutes to 1 hour
        activities.append((activity_hour, activity_minute, duration))
        
        if random.random() < 0.2:
            second_hour = (activity_hour + 6) % 24
            second_minute = random.randint(0, 59)
            second_duration = random.randint(15, 60)
            activities.append((second_hour, second_minute, second_duration))
    
    return activities

def apply_circadian_rhythm(hour: int, profile: PatientProfile) -> float:
    """Apply time-of-day effects to glucose"""

    if 4 <= hour <= 8:
        return profile.dawn_effect * random.uniform(5, 15)
    
    elif 0 <= hour <= 3:
        return -profile.nocturnal_drop * random.uniform(5, 15)
    
    return 0

def calculate_prediction_features(glucose_sequence: List[int]) -> Dict:
    """Calculate features for prediction including slopes and accelerations"""
    
    features = {}
    
    slopes = []
    for i in range(1, len(glucose_sequence)):
        slopes.append(glucose_sequence[i] - glucose_sequence[i-1])
    
    slopes = [0] + slopes
    
    accelerations = []
    for i in range(1, len(slopes)):
        accelerations.append(slopes[i] - slopes[i-1])
    
    accelerations = [0] + accelerations
    
    features["slopes"] = slopes
    features["accelerations"] = accelerations
    
    return features

def is_coma_risk(glucose_values: List[int], slopes: List[float], accelerations: List[float]) -> bool:
    """Determine if there's a risk of diabetic coma based on multiple criteria"""
    
    if any(g <= SEVERE_HYPOGLYCEMIA_THRESHOLD for g in glucose_values):
        return True
        
    if any(g >= SEVERE_HYPERGLYCEMIA_THRESHOLD for g in glucose_values):
        return True
    
    if any(s <= COMA_SLOPE_THRESHOLD for s in slopes):
        return True
        
    if any(s <= WARNING_SLOPE_THRESHOLD and a <= -10 for s, a in zip(slopes, accelerations)):
        return True
        
    low_indices = [i for i, g in enumerate(glucose_values) if g < HYPOGLYCEMIA_THRESHOLD]
    for i in low_indices:
        if i > 0 and slopes[i] < -10:
            return True
            
    return False

def generate_hour_data(
    hour: int,
    day: int,
    starting_glucose: int,
    previous_slope: float,
    profile: PatientProfile,
    meal_schedule: List[Tuple[int, int]],
    activity_schedule: List[Tuple[int, int, int]],
    meal_effects: Dict[int, float],
    activity_effects: Dict[int, float]
) -> Tuple[List[Dict], int, float]:
    """Generate glucose data for one hour"""
    
    hour_data = []
    glucose = starting_glucose
    
    active_meal_effect = 0
    active_activity_effect = 0
    
    for minute in range(MEASUREMENTS_PER_HOUR):
        current_time_minutes = hour * 60 + minute
        
        if current_time_minutes in meal_effects:
            active_meal_effect += meal_effects[current_time_minutes]
        
        if current_time_minutes in activity_effects:
            active_activity_effect += activity_effects[current_time_minutes]
        
        active_meal_effect *= (1 - profile.recovery_rate/60)
        active_activity_effect *= (1 - profile.recovery_rate/60)
        
        baseline_effect = (profile.baseline_glucose - glucose) * profile.recovery_rate / 60
        
        circadian_effect = apply_circadian_rhythm(hour, profile) / 60
        
        noise = random.uniform(-2, 2) * profile.glucose_volatility
        
        delta = (
            active_meal_effect + 
            active_activity_effect + 
            baseline_effect + 
            circadian_effect + 
            noise
        )
        
        event_roll = random.random()
        if event_roll < CRITICAL_DROP_PROB * profile.hypo_risk:
            delta = -random.uniform(30, 60) / 60  # Spread over a minute
        elif event_roll < (CRITICAL_DROP_PROB * profile.hypo_risk + CRITICAL_SPIKE_PROB * profile.hyper_risk):
            delta = random.uniform(30, 60) / 60  # Spread over a minute
        elif event_roll < (CRITICAL_DROP_PROB * profile.hypo_risk + CRITICAL_SPIKE_PROB * profile.hyper_risk + SEVERE_EVENT_PROB):
            if random.random() < 0.5:
                glucose = random.randint(20, SEVERE_HYPOGLYCEMIA_THRESHOLD - 1)
            else:
                glucose = random.randint(SEVERE_HYPERGLYCEMIA_THRESHOLD + 1, 600)
            delta = 0
        
        new_glucose = max(20, min(600, glucose + delta))
        
        if hour == 0 and day == 0 and minute == 0:
            slope = 0
            acceleration = 0
        else:
            slope = new_glucose - glucose
            acceleration = slope - previous_slope
        
        hour_data.append({
            "glucose": int(round(new_glucose)),
            "slope": slope,
            "acceleration": acceleration,
            "time": current_time_minutes
        })
        
        previous_slope = slope
        glucose = new_glucose
    
    return hour_data, glucose, previous_slope

def calculate_meal_and_activity_effects(
    day_in_minutes: int,
    profile: PatientProfile,
    meal_schedule: List[Tuple[int, int]],
    activity_schedule: List[Tuple[int, int, int]]
) -> Tuple[Dict[int, float], Dict[int, float]]:
    """Calculate minute-by-minute effects of meals and activities"""
    
    meal_effects = {}
    activity_effects = {}
    
    for meal_hour, meal_minute in meal_schedule:
        meal_time = meal_hour * 60 + meal_minute
        actual_time = day_in_minutes + meal_time
        
        meal_size = random.uniform(0.5, 2.0)
        
        for i in range(profile.meal_delay, profile.meal_delay + 120):
            if i < 30:
                effect_strength = (i - profile.meal_delay) / 30 * meal_size
            else:
                effect_strength = max(0, (1 - (i - 30) / 90)) * meal_size
                
            effect_minute = actual_time + i
            meal_effect = effect_strength * 15 * profile.meal_response
            
            if effect_minute not in meal_effects:
                meal_effects[effect_minute] = 0
                
            meal_effects[effect_minute] += meal_effect
    
    for activity_hour, activity_minute, duration in activity_schedule:
        activity_time = activity_hour * 60 + activity_minute
        actual_time = day_in_minutes + activity_time
        
        intensity = random.uniform(0.5, 1.5)
        
        for i in range(duration + 60):
            if i < duration:
                effect_strength = intensity
            else:
                effect_strength = intensity * (1 - (i - duration) / 60)
                
            effect_minute = actual_time + i
            activity_effect = -effect_strength * 10 * profile.activity_response
            
            if effect_minute not in activity_effects:
                activity_effects[effect_minute] = 0
                
            activity_effects[effect_minute] += activity_effect
    
    return meal_effects, activity_effects

def generate(output: str, time=30, additional=True) -> None:
    """Generate glucose data for multiple patients over time"""
    
    all_data = []

    for patient_idx in range(PATIENT_COUNT):
        patient_id = str(uuid.uuid4())[:8] 
        profile = PatientProfile(patient_id)
        
        days = random.randint(MIN_DAYS, time)
        
        glucose = profile.baseline_glucose + random.randint(-15, 15)
        previous_slope = 0
        
        for day in range(days):
            meal_schedule = generate_meal_schedule()
            activity_schedule = generate_activity_schedule()
            
            day_start_minutes = day * 24 * 60
            meal_effects, activity_effects = calculate_meal_and_activity_effects(
                day_start_minutes, profile, meal_schedule, activity_schedule
            )
            
            for hour in range(24):
                hour_data, glucose, previous_slope = generate_hour_data(
                    hour, 
                    day,
                    glucose, 
                    previous_slope, 
                    profile,
                    meal_schedule,
                    activity_schedule,
                    meal_effects,
                    activity_effects
                )
                
                glucose_values = [item['glucose'] for item in hour_data]
                slopes = [item['slope'] for item in hour_data]
                accelerations = [item['acceleration'] for item in hour_data]
                
                label = "1" if is_coma_risk(glucose_values, slopes, accelerations) else "0"
                
                all_data.append({
                    "patient_id": patient_id,
                    "day": day,
                    "hour": hour,
                    "glucose_values": glucose_values,
                    "slopes": slopes,
                    "accelerations": accelerations,
                    "label": label
                })
    
    processed_data = []
    for patient_id in set(item["patient_id"] for item in all_data):
        patient_data = [item for item in all_data if item["patient_id"] == patient_id]
        patient_data.sort(key=lambda x: (x["day"], x["hour"]))
        
        for i in range(len(patient_data) - 1):
            current_hour = patient_data[i]
            next_hour = patient_data[i + 1]
            
            if (current_hour["day"] == next_hour["day"] and current_hour["hour"] + 1 == next_hour["hour"]) or \
               (current_hour["day"] + 1 == next_hour["day"] and current_hour["hour"] == 23 and next_hour["hour"] == 0):
                current_hour["future_label"] = next_hour["label"]
                processed_data.append(current_hour)
    
    positive_samples = [item for item in processed_data if item["future_label"] == "1"]
    negative_samples = [item for item in processed_data if item["future_label"] == "0"]
    
    if len(positive_samples) < len(negative_samples) / 3:
        sample_size = len(positive_samples) * 3
        if sample_size < len(negative_samples):
            negative_samples = random.sample(negative_samples, sample_size)
    
    balanced_data = positive_samples + negative_samples
    random.shuffle(balanced_data)
    
    fieldnames = [f"glucose_{i}" for i in range(1, MEASUREMENTS_PER_HOUR + 1)]
    
    if additional:
        fieldnames += [f"slope_{i}" for i in range(1, MEASUREMENTS_PER_HOUR + 1)]
        fieldnames += [f"acceleration_{i}" for i in range(1, MEASUREMENTS_PER_HOUR + 1)]
    
    fieldnames += ["future_label"]
    
    with open(output, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in balanced_data:
            flat_row = {
                "future_label": row["future_label"]
            }
            
            flat_row.update({f"glucose_{i+1}": row["glucose_values"][i] for i in range(MEASUREMENTS_PER_HOUR)})
            
            if additional:
                flat_row.update({f"slope_{i+1}": row["slopes"][i] for i in range(MEASUREMENTS_PER_HOUR)})
                flat_row.update({f"acceleration_{i+1}": row["accelerations"][i] for i in range(MEASUREMENTS_PER_HOUR)})
            
            writer.writerow(flat_row)