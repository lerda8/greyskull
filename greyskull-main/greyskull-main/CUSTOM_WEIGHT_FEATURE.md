# ✨ Custom Next Weight Feature

## Overview
Added the ability to override the automatic next weight calculation when logging workouts. This gives you full control over your progression.

## How It Works

### Default Behavior (Automatic)
- **10+ reps**: Increase by 2.5 kg
- **5-9 reps**: Increase by 1.5 kg  
- **< 5 reps**: Reduce by 10%

### Custom Override
Now you can click "Customize" and enter your own next weight, even if you hit 10+ reps but want to stay at the same weight or increase more/less.

## Features

### 1. **Live Auto-Calculation**
- As you change the current weight or reps category, the suggested next weight updates in real-time
- You can see what the app recommends before deciding to customize

### 2. **Easy Toggle**
- Click "Customize" to enter a custom weight
- Click "Use Auto" to go back to the automatic calculation
- The automatic suggestion is always visible for reference

### 3. **Mobile & Desktop**
- Works on both the mobile view (iPhone 12 Mini) and desktop view
- Touch-friendly interface on mobile
- Smooth transitions and clear visual feedback

### 4. **Validation**
- Custom weights are validated (0-1000 kg range)
- Must be a valid number
- Falls back to auto-calculation if no custom weight provided

## UI Changes

### Mobile View
- Dashed border box showing next weight
- "Customize" button in top-right corner
- Large, centered display of suggested weight
- When customized, shows both custom input and auto suggestion for reference

### Desktop View  
- Green-tinted box for next weight section
- Same toggle functionality
- Integrated into the workout logging form
- Consistent with mobile experience

## Code Changes

### Backend (`app.py`)
- Updated `web_log_workout()` to accept optional `custom_next_weight` parameter
- Updated `save_workout()` API endpoint for consistency
- Added validation for custom weight values
- Falls back to `calculate_next_weight()` if no custom value provided

### Frontend
- **Mobile** (`templates/exercise_mobile.html`): JavaScript to handle toggle and live updates
- **Desktop** (`templates/exercise.html`): Same functionality with desktop-appropriate styling
- Both versions use the same calculation logic for consistency

## Use Cases

1. **Conservative Progression**: Hit 10+ reps but want to repeat the weight
2. **Deload Planning**: Manually set a lower weight for deload week
3. **Equipment Limitations**: Gym only has certain plate increments
4. **Feel-Based Training**: Felt particularly strong/weak and want to adjust accordingly
5. **Injury Recovery**: Gradual return with custom micro-progressions

## API Support

The feature also works via the API endpoint `/api/workout`:

```json
POST /api/workout
{
  "exercise_id": "abc123",
  "weight": 100,
  "reps_category": "more_than_10",
  "custom_next_weight": 102.5  // Optional
}
```

If `custom_next_weight` is omitted, the automatic calculation is used.
