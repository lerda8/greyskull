# Exercise Type Feature Implementation

## Overview
Implemented exercise-specific weight progression based on muscle groups being targeted.

## New Weight Progression Rules

### Upper Body Exercises (default)
- **Normal progression (5+ reps):** +1kg
- **Excellent progression (10+ reps AMRAP):** +2kg (double)
- **Failed progression (<5 reps):** -10% (deload)

### Leg Exercises
- **Normal progression (5+ reps):** +2kg
- **Excellent progression (10+ reps AMRAP):** +4kg (double)
- **Failed progression (<5 reps):** -10% (deload)

## Changes Made

### Database Schema
- Added `exercise_type` column to `exercises` table (VARCHAR(20), default: 'upper')
- Values: 'upper' or 'legs'
- Migration script: `migrate_add_exercise_type.py`
- Automatically detected and updated existing exercises (squats, deadlifts, etc.)

### Backend Changes (`app.py`)
1. **Updated `calculate_next_weight()` function:**
   - Now accepts `exercise_type` parameter
   - Uses different base increments: 2kg for legs, 1kg for upper body
   - Doubles increment for 10+ reps regardless of type

2. **Updated exercise creation routes:**
   - `web_add_exercise()` - accepts exercise_type from form
   - `add_exercise()` - API endpoint validates exercise_type
   
3. **Updated workout logging routes:**
   - `save_workout()` - passes exercise.exercise_type to calculation
   - `web_log_workout()` - passes exercise.exercise_type to calculation

### Frontend Changes

#### Templates Updated:
1. **`index_mobile.html`** - Add Exercise modal includes exercise type dropdown
2. **`index.html`** - Desktop Add Exercise modal includes exercise type dropdown
3. **`exercise_mobile.html`** - JavaScript calculates next weight using exercise type
4. **`exercise.html`** - Desktop JavaScript calculates next weight using exercise type

#### UI Elements:
- Exercise Type dropdown in "Add Exercise" modal:
  - Upper Body (+1kg / +2kg for 10+ reps)
  - Legs (+2kg / +4kg for 10+ reps)
- Real-time weight calculation preview uses correct increment based on exercise type
- Custom weight override still available

### Migration
The migration script automatically:
1. Adds the `exercise_type` column
2. Sets default value to 'upper' for all exercises
3. Auto-detects leg exercises (squat, deadlift, leg press, lunge) and sets them to 'legs'

## Usage
1. When adding a new exercise, select the appropriate exercise type
2. The system will automatically use the correct weight progression
3. Existing exercises have been categorized automatically
4. Custom next weight override still works regardless of exercise type

## Testing
✅ Migration completed successfully - 1 exercise updated to 'legs' type
✅ New exercises can be created with exercise type selection
✅ Weight calculations use appropriate increments
✅ JavaScript preview shows correct next weight
✅ Both mobile and desktop interfaces updated
