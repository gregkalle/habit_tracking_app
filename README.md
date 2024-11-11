# Habit Tracking App
Habit Tracking App is an application to track your daily and weekly tasks to build good and break bad habits.  

## Installation
Download the repository:
```bash
gh repo clone gregkalle/habit_tracking_app
```
Install the setup.py:
```bash
pip install --editable .
```
## Usage
To run the habit tracking app, use the following command:
```bash
habits
```
### Check Date
To check a date on which your habit was fulfilled, selected a habit and click the "check date"-button. Selcted a date and click the "selected date"-button to mark the date fulfilled. Click the "today"-button to mark today fulfilled. Click the "Cancel"-button to close the "select date"-window without marking.

Make sure to only select one habit to check.

### Create New Habit
To create a new task, click the "new habit"-button. Enter the habit name, the habit description and a frequency. Click the "OK"-button, to save the new habit to the database or click the "Cancel"-button to close the "new habit"-window without changes.

### Change Habit
To change an existing habit, select a habit and click the "change habit"-button. Enter the new name or description. Click the "OK"-button, to save the changed habit name or description to the database or click the "Cancel"-button to close the "change habit"-window without changes.

Make sure to only select one habit to change.

### Delete Habit
To delete a habit from the database, select the habit and click the "delete habit"-button. Click the "OK"-button, to delete the selected habit from the database or click the "Cancel"-button to close the "Delete"-window without changes.

Make sure to only select one habit to delete.

### Calendar
To show a calendar with the createn date and all marked dates of the habit, click the "calendar"-button.
- The createn date is red with white number, if createn date is not marked.
- The createn date is red with green number, if createn date is marked.
- First date of the period in which the habit was fulfilled is green. If the frequency is one, it is the date on which the habit was fulfilled.
- The other dates of the period in which the habit was fulfilled are light green. They are only shown if the habit frequency is not daily (1).

Make sure to only select one habit to show calendar.

### Show Habits
To show the daily, weekly, all selcted or all habits in the app, select the shown habits with the "show habits"-button.

## License

[MIT](https://choosealicense.com/licenses/mit/)
