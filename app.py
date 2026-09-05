import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timezone


# ============================================================
# QUESTIONS
# ============================================================

QUESTIONS = [
    {'topic': 'Python', 'q': 'What is the output of `x=[1,2,3]; y=x; y.append(4); print(x)`?', 'opts': ['[1, 2, 3]', '[1, 2, 3, 4]', '[4]', 'Error'], 'a': 1, 'e': 'Both names refer to the same list object.'},
    {'topic': 'Python', 'q': 'Which structure is ordered and mutable?', 'opts': ['Tuple', 'List', 'Set', 'Frozen set'], 'a': 1, 'e': 'Lists are ordered and mutable.'},
    {'topic': 'Python', 'q': 'What is `7 // 2`?', 'opts': ['3', '3.5', '4', '1'], 'a': 0, 'e': 'Floor division gives 3.'},
    {'topic': 'Python', 'q': 'Which keyword defines a function?', 'opts': ['func', 'define', 'def', 'function'], 'a': 2, 'e': 'Python uses def.'},
    {'topic': 'Python', 'q': 'What does `range(2,7)` contain?', 'opts': ['2,3,4,5,6', '2,3,4,5,6,7', '1,2,3,4,5,6', '3,4,5,6,7'], 'a': 0, 'e': 'The stop value is excluded.'},
    {'topic': 'Python', 'q': 'A function without a return statement returns:', 'opts': ['0', 'False', 'None', 'Empty string'], 'a': 2, 'e': 'Python implicitly returns None.'},
    {'topic': 'Python', 'q': 'Which operator tests object identity?', 'opts': ['==', '=', 'is', '!='], 'a': 2, 'e': 'is checks whether references point to the same object.'},
    {'topic': 'Python', 'q': 'What does a dictionary store?', 'opts': ['Only numbers', 'Key-value pairs', 'Only strings', 'Only unique values'], 'a': 1, 'e': 'Dictionaries map keys to values.'},
    {'topic': 'Python', 'q': 'What does `bool([])` return?', 'opts': ['True', 'False', 'None', 'Error'], 'a': 1, 'e': 'An empty list is falsy.'},
    {'topic': 'Python', 'q': 'Which statement skips to the next loop iteration?', 'opts': ['break', 'continue', 'pass', 'skip'], 'a': 1, 'e': 'continue skips the current iteration.'},
    {'topic': 'Python', 'q': 'Which statement terminates the nearest loop?', 'opts': ['stop', 'exit', 'break', 'continue'], 'a': 2, 'e': 'break exits the nearest loop.'},
    {'topic': 'Python', 'q': 'What does `try/except` help with?', 'opts': ['Runtime error handling', 'Image resizing', 'Model normalization', 'Plotting'], 'a': 0, 'e': 'It catches and handles exceptions.'},
    {'topic': 'Python', 'q': 'Which is immutable?', 'opts': ['List', 'Dictionary', 'Tuple', 'Set'], 'a': 2, 'e': 'Tuples cannot be changed after creation.'},
    {'topic': 'Python', 'q': 'What does `*args` collect?', 'opts': ['Extra positional arguments', 'Extra keyword arguments', 'Only strings', 'Only integers'], 'a': 0, 'e': '*args collects positional arguments.'},
    {'topic': 'Python', 'q': 'What does `**kwargs` collect?', 'opts': ['Extra positional arguments', 'Extra keyword arguments', 'Only lists', 'Only integers'], 'a': 1, 'e': '**kwargs collects keyword arguments.'},
    {'topic': 'Python', 'q': 'What does `len([10,20,30,40])` return?', 'opts': ['3', '4', '5', '40'], 'a': 1, 'e': 'There are four elements.'},
    {'topic': 'Python', 'q': 'Which is a valid list comprehension?', 'opts': ['[x*2 for x in nums]', 'for x in nums: x*2', 'list x*2 nums', '[for x*2 in nums]'], 'a': 0, 'e': 'The first form is valid list-comprehension syntax.'},
    {'topic': 'Python', 'q': 'What is the result of `10 % 3`?', 'opts': ['0', '1', '3', '3.33'], 'a': 1, 'e': 'Modulo returns the remainder, 1.'},
    {'topic': 'Python', 'q': 'Why use functions in larger programs?', 'opts': ['Reuse and organization', 'Guaranteed accuracy', 'No bugs', 'No memory use'], 'a': 0, 'e': 'Functions improve reuse and maintainability.'},
    {'topic': 'Python', 'q': 'What does `import math` do?', 'opts': ['Loads the math module', 'Creates a class', 'Starts a loop', 'Creates a DataFrame'], 'a': 0, 'e': 'import loads a module for use.'},

    {'topic': 'NumPy', 'q': 'What is the shape of `np.array([[1,2,3],[4,5,6]])`?', 'opts': ['(2,3)', '(3,2)', '(6,)', '(2,2)'], 'a': 0, 'e': 'There are 2 rows and 3 columns.'},
    {'topic': 'NumPy', 'q': 'What is `np.array([1,2,3]) + np.array([10,20,30])`?', 'opts': ['[11,22,33]', '[10,40,90]', '[1,2,3,10,20,30]', 'Error'], 'a': 0, 'e': 'NumPy adds compatible arrays element-wise.'},
    {'topic': 'NumPy', 'q': 'What must hold for reshaping a six-element array to `(2,3)`?', 'opts': ['Exactly 6 elements', 'Exactly 5', 'Exactly 8', 'Any count'], 'a': 0, 'e': '2×3 requires six elements.'},
    {'topic': 'NumPy', 'q': "Which property gives an array's dimensions?", 'opts': ['size', 'shape', 'dtype', 'itemsize'], 'a': 1, 'e': 'shape reports the size of each axis.'},
    {'topic': 'NumPy', 'q': 'Which property gives the number of axes?', 'opts': ['shape', 'ndim', 'size', 'dtype'], 'a': 1, 'e': 'ndim is the number of dimensions.'},
    {'topic': 'NumPy', 'q': 'What does `np.mean(x)` calculate?', 'opts': ['Maximum', 'Average', 'Minimum', 'Variance'], 'a': 1, 'e': 'mean calculates the arithmetic average.'},
    {'topic': 'NumPy', 'q': 'What does `np.zeros((2,3))` create?', 'opts': ['2×3 zeros', '3×3 zeros', '2×2 zeros', 'Six random values'], 'a': 0, 'e': 'The requested shape is 2 by 3.'},
    {'topic': 'NumPy', 'q': 'What does `x[1:4]` select?', 'opts': ['Indices 1,2,3', 'Indices 1,2,3,4', 'Indices 0,1,2,3', 'Only index 4'], 'a': 0, 'e': 'The stop index is excluded.'},
    {'topic': 'NumPy', 'q': 'What is broadcasting?', 'opts': ['Compatible different shapes can participate in operations', 'Saving arrays', 'Training models', 'Plotting'], 'a': 0, 'e': 'Broadcasting expands compatible shapes conceptually.'},
    {'topic': 'NumPy', 'q': 'Which function returns the maximum?', 'opts': ['np.high', 'np.max', 'np.large', 'np.top'], 'a': 1, 'e': 'np.max returns the maximum value.'},
    {'topic': 'NumPy', 'q': 'What does dtype describe?', 'opts': ['Element data type', 'Array shape', 'Row count', 'File type'], 'a': 0, 'e': 'dtype identifies stored element type.'},
    {'topic': 'NumPy', 'q': 'For `x=np.array([1,2,3])`, what is `x*2`?', 'opts': ['[2,4,6]', '[1,2,3,2]', '[3,4,5]', 'Error'], 'a': 0, 'e': 'Scalar multiplication is element-wise.'},
    {'topic': 'NumPy', 'q': 'Why is vectorization useful?', 'opts': ['Efficient numerical operations without explicit Python loops', 'Deletes data', 'Creates labels', 'Prevents overfitting'], 'a': 0, 'e': 'Vectorized operations are concise and efficient.'},
    {'topic': 'NumPy', 'q': 'What does `np.unique(x)` return?', 'opts': ['Unique values', 'Duplicates only', 'Mean', 'Shape'], 'a': 0, 'e': 'It returns unique values.'},
    {'topic': 'NumPy', 'q': 'What does `np.sum(x, axis=0)` on a 2D array do?', 'opts': ['Column-wise sums', 'Row-wise sums', 'Only flattening', 'Maximum values'], 'a': 0, 'e': 'axis=0 reduces the row axis, producing column sums.'},

    {'topic': 'Pandas', 'q': 'Which Pandas object is designed for tabular rows and columns?', 'opts': ['Series', 'DataFrame', 'Tensor', 'Scalar'], 'a': 1, 'e': 'DataFrame is two-dimensional tabular data.'},
    {'topic': 'Pandas', 'q': 'Which calculates a column mean?', 'opts': ["df['Age'].mean()", "df['Age'].average()", 'df.mean_age()', "df.avg('Age')"], 'a': 0, 'e': 'Series provides mean().'},
    {'topic': 'Pandas', 'q': 'What does `df.isnull().sum()` commonly provide?', 'opts': ['Missing count per column', 'Row averages', 'Duplicates', 'Column names'], 'a': 0, 'e': 'isnull marks missing values and sum counts them.'},
    {'topic': 'Pandas', 'q': 'What does `df.dropna()` do by default?', 'opts': ['Drops rows with missing values', 'Fills missing values', 'Sorts rows', 'Duplicates rows'], 'a': 0, 'e': 'Default dropna removes rows containing missing values.'},
    {'topic': 'Pandas', 'q': 'What does `fillna()` do?', 'opts': ['Fills missing values', 'Deletes columns', 'Creates plots', 'Splits data'], 'a': 0, 'e': 'fillna replaces missing values.'},
    {'topic': 'Pandas', 'q': 'What does `df.head()` show?', 'opts': ['First rows', 'Last rows', 'Random rows', 'Only numeric rows'], 'a': 0, 'e': 'head shows the first rows.'},
    {'topic': 'Pandas', 'q': 'What does `df.tail()` show?', 'opts': ['First rows', 'Last rows', 'Random rows', 'Only missing rows'], 'a': 1, 'e': 'tail shows the last rows.'},
    {'topic': 'Pandas', 'q': 'What does `df.info()` help inspect?', 'opts': ['Structure, dtypes and non-null counts', 'Only means', 'Only duplicates', 'Only plots'], 'a': 0, 'e': 'info summarizes DataFrame structure.'},
    {'topic': 'Pandas', 'q': 'Which method identifies duplicate rows?', 'opts': ['df.duplicates()', 'df.duplicated()', 'df.repeat()', 'df.same()'], 'a': 1, 'e': 'duplicated returns a Boolean mask for duplicate rows.'},
    {'topic': 'Pandas', 'q': "What does `df['Age']` select?", 'opts': ['Age column', 'Age row', 'Whole DataFrame', 'Missing values only'], 'a': 0, 'e': 'Column-label selection returns that Series.'},
    {'topic': 'Pandas', 'q': '`loc` is primarily based on:', 'opts': ['Labels', 'Integer positions', 'Randomness', 'Dtypes'], 'a': 0, 'e': 'loc is label-based.'},
    {'topic': 'Pandas', 'q': '`iloc` is primarily based on:', 'opts': ['Labels', 'Integer positions', 'Column names only', 'Missing values'], 'a': 1, 'e': 'iloc is integer-position-based.'},
    {'topic': 'Pandas', 'q': 'Why learn preprocessing statistics from training data only?', 'opts': ['To reduce leakage', 'To increase image size', 'To remove Python', 'To guarantee 100% accuracy'], 'a': 0, 'e': 'Using validation/test information can leak information into training.'},
    {'topic': 'Pandas', 'q': 'What does groupby enable?', 'opts': ['Grouped aggregation and analysis', 'Convolution', 'Gradient calculation', 'Compilation'], 'a': 0, 'e': 'groupby supports split-apply-combine analysis.'},
    {'topic': 'Pandas', 'q': 'What does `pd.read_csv()` commonly do?', 'opts': ['Loads CSV into a DataFrame', 'Creates a CNN', 'Saves a model', 'Plots data'], 'a': 0, 'e': 'read_csv reads CSV data into a DataFrame.'},

    {'topic': 'Deep Learning', 'q': 'What is the main purpose of an activation function?', 'opts': ['Introduce non-linearity', 'Store datasets', 'Split data', 'Increase disk space'], 'a': 0, 'e': 'Nonlinear activations let networks learn nonlinear mappings.'},
    {'topic': 'Deep Learning', 'q': 'What does a loss function measure?', 'opts': ['Prediction error relative to targets', 'Number of layers', 'Image width', 'GPU memory'], 'a': 0, 'e': 'Loss quantifies model error according to the objective.'},
    {'topic': 'Deep Learning', 'q': 'What does backpropagation calculate?', 'opts': ['Gradients for trainable parameters', 'Labels', 'CSV rows', 'Filenames'], 'a': 0, 'e': 'Backpropagation computes gradients of loss.'},
    {'topic': 'Deep Learning', 'q': 'What does an optimizer do?', 'opts': ['Updates trainable parameters using gradients', 'Loads images', 'Creates labels', 'Only calculates accuracy'], 'a': 0, 'e': 'Optimizers use gradients to update weights.'},
    {'topic': 'Deep Learning', 'q': 'What is one epoch?', 'opts': ['One complete pass through training data', 'One neuron', 'One class', 'One batch only'], 'a': 0, 'e': 'An epoch covers the full training dataset once.'},
    {'topic': 'Deep Learning', 'q': 'What is a batch?', 'opts': ['A subset processed together', 'A complete model', 'A class label', 'A loss function'], 'a': 0, 'e': 'A batch is a group of samples processed together.'},
    {'topic': 'Deep Learning', 'q': 'What does learning rate control?', 'opts': ['Update step size', 'Number of classes', 'Image channels', 'Dataset size'], 'a': 0, 'e': 'It controls optimizer update magnitude.'},
    {'topic': 'Deep Learning', 'q': 'High training accuracy but low validation accuracy suggests:', 'opts': ['Overfitting', 'Underfitting', 'No training', 'Perfect generalization'], 'a': 0, 'e': 'The model fits training data but generalizes poorly.'},
    {'topic': 'Deep Learning', 'q': 'Low training and validation accuracy can indicate:', 'opts': ['Underfitting', 'Overfitting only', 'Perfect fit', 'No possible problem'], 'a': 0, 'e': 'Poor training performance can indicate underfitting.'},
    {'topic': 'Deep Learning', 'q': 'What is validation data mainly used for?', 'opts': ['Monitoring generalization during development', 'Replacing training data', 'Guaranteeing test accuracy', 'Creating GPUs'], 'a': 0, 'e': 'Validation data supports development and tuning decisions.'},
    {'topic': 'Deep Learning', 'q': 'What is test data ideally used for?', 'opts': ['Final evaluation after development', 'Repeated tuning', 'Fitting preprocessing statistics', 'Training weights'], 'a': 0, 'e': 'A held-out test set estimates final generalization.'},
    {'topic': 'Deep Learning', 'q': 'What is data leakage?', 'opts': ['Improper use of information across the evaluation boundary', 'Random shuffling', 'Image resizing', 'Using batches'], 'a': 0, 'e': 'Leakage occurs when information that should be unavailable influences development.'},
    {'topic': 'Deep Learning', 'q': 'Which can reduce overfitting?', 'opts': ['Regularization', 'Always increasing epochs', 'Removing validation data', 'Using test labels'], 'a': 0, 'e': 'Regularization can improve generalization.'},
    {'topic': 'Deep Learning', 'q': 'What does dropout do during training?', 'opts': ['Randomly disables some activations', 'Adds labels', 'Increases pixels', 'Calculates test accuracy'], 'a': 0, 'e': 'Dropout randomly removes activations as a regularizer.'},
    {'topic': 'Deep Learning', 'q': 'What is batch normalization generally doing?', 'opts': ['Normalizing activations using batch statistics during training', 'Normalizing class names', 'Renaming files', 'Calculating test accuracy'], 'a': 0, 'e': 'Batch normalization uses batch statistics to normalize activations.'},
    {'topic': 'Deep Learning', 'q': 'What is a hyperparameter?', 'opts': ['A setting chosen rather than directly learned as a weight', 'A target label', 'A gradient', 'A pixel'], 'a': 0, 'e': 'Examples include learning rate and batch size.'},
    {'topic': 'Deep Learning', 'q': 'Why scale image pixels from 0–255 to 0–1?', 'opts': ['Provide a smaller consistent numerical range', 'Add classes', 'Increase resolution', 'Remove labels'], 'a': 0, 'e': 'Division by 255 scales the values to 0–1.'},
    {'topic': 'Deep Learning', 'q': 'What is transfer learning?', 'opts': ['Using a pretrained model as a starting point', 'Training without data', 'Deleting features', 'Changing labels only'], 'a': 0, 'e': 'Transfer learning reuses learned representations.'},

    {'topic': 'CNN & Training', 'q': 'What is the main purpose of convolution layers for images?', 'opts': ['Learn spatial features', 'Convert directly to labels', 'Remove pixels', 'Guarantee no overfitting'], 'a': 0, 'e': 'Convolutions learn local spatial patterns.'},
    {'topic': 'CNN & Training', 'q': 'What does a CNN kernel/filter learn?', 'opts': ['Feature patterns', 'Class names directly', 'File extensions', 'Epoch counts'], 'a': 0, 'e': 'Kernel weights learn local feature detectors.'},
    {'topic': 'CNN & Training', 'q': 'What does max pooling usually do?', 'opts': ['Keeps maximum values from local regions', 'Adds pixels', 'Calculates loss', 'Changes labels'], 'a': 0, 'e': 'Max pooling summarizes local regions.'},
    {'topic': 'CNN & Training', 'q': 'An RGB image 128×128×3 has 3 because of:', 'opts': ['Three color channels', 'Three classes', 'Three filters', 'Three layers'], 'a': 0, 'e': 'RGB has red, green and blue channels.'},
    {'topic': 'CNN & Training', 'q': 'Why use Flatten before dense layers?', 'opts': ['Convert feature maps into a vector', 'Increase resolution', 'Delete features', 'Normalize labels'], 'a': 0, 'e': 'Flatten changes a multi-dimensional feature map to a vector.'},
    {'topic': 'CNN & Training', 'q': 'What does stride control in convolution?', 'opts': ['How far the filter moves each step', 'Number of classes', 'Learning rate', 'Epoch count'], 'a': 0, 'e': 'Stride specifies the spatial step.'},
    {'topic': 'CNN & Training', 'q': 'What does same padding generally aim to do with stride 1?', 'opts': ['Preserve spatial dimensions', 'Remove all borders', 'Double channels', 'Set batch size'], 'a': 0, 'e': 'Same padding maintains spatial size for stride 1.'},
    {'topic': 'CNN & Training', 'q': 'Why can deeper CNN layers learn more complex features?', 'opts': ['They combine representations from earlier layers', 'They use no weights', 'They ignore earlier layers', 'They see only labels'], 'a': 0, 'e': 'Later layers build on earlier learned representations.'},
    {'topic': 'CNN & Training', 'q': 'Training loss decreases while validation loss increases. Most likely:', 'opts': ['Overfitting', 'Underfitting', 'No optimization', 'Data deletion'], 'a': 0, 'e': 'Training improves while validation generalization worsens.'},
    {'topic': 'CNN & Training', 'q': 'If learning rate is far too high, training may:', 'opts': ['Oscillate or diverge', 'Always become perfect', 'Stop using gradients', 'Remove labels'], 'a': 0, 'e': 'Large updates can overshoot useful parameter regions.'},
    {'topic': 'CNN & Training', 'q': 'If learning rate is extremely small, training may:', 'opts': ['Converge very slowly', 'Overfit immediately', 'Increase image size', 'Disable backpropagation'], 'a': 0, 'e': 'Very small updates slow optimization.'},
    {'topic': 'CNN & Training', 'q': 'Why save the best validation checkpoint?', 'opts': ['Retain a version with stronger validation performance', 'Increase dataset size', 'Remove test data', 'Guarantee deployment success'], 'a': 0, 'e': 'Checkpointing preserves a strong validation-performing version.'},
]


# ============================================================
# SETTINGS
# ============================================================

TIME_LIMIT = 90 * 60
PASS_PERCENT = 60

RESULT_COLUMNS = [
    "timestamp",
    "student_name",
    "score",
    "total",
    "percentage",
    "grade",
    "status",
    "python",
    "numpy",
    "pandas",
    "deep_learning",
    "cnn_training",
]

st.set_page_config(
    page_title="Python & Deep Learning Quiz",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def grade_for(p):
    """Return grade based on percentage."""
    if p >= 90:
        return "A+"
    elif p >= 80:
        return "A"
    elif p >= 70:
        return "B"
    elif p >= 60:
        return "C"
    else:
        return "F"


def local_results():
    """Load locally saved results."""
    try:
        return pd.read_csv("quiz_results.csv")
    except Exception:
        return pd.DataFrame(columns=RESULT_COLUMNS)


def make_result():
    """Create a result record."""
    score = st.session_state.score
    total = len(st.session_state.questions)

    pct = (score / total * 100) if total else 0

    topics = {}

    for i, q in enumerate(st.session_state.questions):
        topic = q["topic"]

        if topic not in topics:
            topics[topic] = [0, 0]

        topics[topic][1] += 1

        if st.session_state.answers.get(i) == q["a"]:
            topics[topic][0] += 1

    return {
        "timestamp": datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),
        "student_name": st.session_state.name,
        "score": score,
        "total": total,
        "percentage": round(pct, 2),
        "grade": grade_for(pct),
        "status": "PASS" if pct >= PASS_PERCENT else "FAIL",

        "python": (
            f"{topics.get('Python', [0, 0])[0]}/"
            f"{topics.get('Python', [0, 0])[1]}"
        ),

        "numpy": (
            f"{topics.get('NumPy', [0, 0])[0]}/"
            f"{topics.get('NumPy', [0, 0])[1]}"
        ),

        "pandas": (
            f"{topics.get('Pandas', [0, 0])[0]}/"
            f"{topics.get('Pandas', [0, 0])[1]}"
        ),

        "deep_learning": (
            f"{topics.get('Deep Learning', [0, 0])[0]}/"
            f"{topics.get('Deep Learning', [0, 0])[1]}"
        ),

        "cnn_training": (
            f"{topics.get('CNN & Training', [0, 0])[0]}/"
            f"{topics.get('CNN & Training', [0, 0])[1]}"
        ),
    }


def save_google(row):
    """Save result to Google Sheets."""
    try:
        conn = st.connection("gsheets", type="gspread")

        ref = st.secrets["connections"]["gsheets"]["spreadsheet"]

        if str(ref).startswith("http"):
            sh = conn.client.open_by_url(ref)
        else:
            sh = conn.client.open_by_key(ref)

        try:
            ws = sh.worksheet("Results")
        except Exception:
            ws = sh.add_worksheet(
                title="Results",
                rows=1000,
                cols=len(RESULT_COLUMNS)
            )

            ws.append_row(RESULT_COLUMNS)

        if not ws.get_all_values():
            ws.append_row(RESULT_COLUMNS)

        ws.append_row(
            [row.get(c, "") for c in RESULT_COLUMNS]
        )

        return True, "Result saved to Google Sheets."

    except Exception as e:
        return False, f"Google Sheets is not configured: {e}"


def persist():
    """Save result locally and to Google Sheets."""
    row = make_result()

    df = local_results()

    updated = pd.concat(
        [df, pd.DataFrame([row])],
        ignore_index=True
    )

    updated.to_csv(
        "quiz_results.csv",
        index=False
    )

    return save_google(row)


# ============================================================
# QUIZ CONTROL
# ============================================================

def start_quiz(name):
    """Start a new quiz attempt."""

    st.session_state.name = name.strip()

    # Randomize question order.
    st.session_state.questions = random.sample(
        QUESTIONS,
        len(QUESTIONS)
    )

    # Empty answer dictionary.
    st.session_state.answers = {}

    st.session_state.start_time = time.time()
    st.session_state.score = 0
    st.session_state.saved = False
    st.session_state.save_ok = False
    st.session_state.save_msg = ""
    st.session_state.screen = "quiz"


def finish():
    """Calculate score and save result."""

    st.session_state.score = sum(
        st.session_state.answers.get(i) == q["a"]
        for i, q in enumerate(st.session_state.questions)
    )

    if not st.session_state.saved:
        ok, msg = persist()

        st.session_state.saved = True
        st.session_state.save_ok = ok
        st.session_state.save_msg = msg

    st.session_state.screen = "result"


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

defaults = {
    "screen": "start",
    "questions": [],
    "answers": {},
    "name": "",
    "start_time": None,
    "score": 0,
    "saved": False,
    "save_ok": False,
    "save_msg": "",
    "teacher": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# TEACHER LOGIN
# ============================================================

def teacher_sidebar():

    st.sidebar.markdown("---")
    st.sidebar.subheader("👨‍🏫 Teacher Login")

    pw = st.sidebar.text_input(
        "syed1234@",
        type="password"
    )

    if st.sidebar.button(
        "Login",
        use_container_width=True
    ):

        try:
            configured = st.secrets["TEACHER_PASSWORD"]
        except Exception:
            configured = None

        if configured and pw == configured:

            st.session_state.teacher = True
            st.rerun()

        elif not configured:

            st.sidebar.error(
                "Set TEACHER_PASSWORD in Streamlit Secrets."
            )

        else:

            st.sidebar.error(
                "Incorrect password."
            )


# ============================================================
# TEACHER DASHBOARD
# ============================================================

def teacher_dashboard():

    st.title("👨‍🏫 Teacher Dashboard")

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.teacher = False
        st.rerun()

    # Start with local results.
    df = local_results()

    # Try Google Sheets.
    try:

        conn = st.connection(
            "gsheets",
            type="gspread"
        )

        ref = st.secrets["connections"]["gsheets"]["spreadsheet"]

        if str(ref).startswith("http"):
            sh = conn.client.open_by_url(ref)
        else:
            sh = conn.client.open_by_key(ref)

        ws = sh.worksheet("Results")

        records = ws.get_all_records()

        if records:
            df = pd.DataFrame(records)

    except Exception:
        pass

    st.subheader("📊 Student Results")

    if df.empty:

        st.info("No submitted results yet.")
        return

    pct = pd.to_numeric(
        df["percentage"],
        errors="coerce"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Students",
        len(df)
    )

    c2.metric(
        "Average",
        f"{pct.mean():.1f}%"
    )

    c3.metric(
        "Passed",
        int(
            (
                df["status"]
                .astype(str)
                .str.upper() == "PASS"
            ).sum()
        )
    )

    c4.metric(
        "Highest",
        f"{pct.max():.1f}%"
    )

    search = st.text_input(
        "🔍 Search student"
    )

    if search:

        view = df[
            df["student_name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    else:

        view = df

    st.dataframe(
        view,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Download Results CSV",
        view.to_csv(index=False).encode("utf-8"),
        "quiz_results.csv",
        "text/csv",
        use_container_width=True
    )


# ============================================================
# TEACHER AREA
# ============================================================

teacher_sidebar()

if st.session_state.get("teacher"):

    teacher_dashboard()

    st.stop()


# ============================================================
# STUDENT HEADER
# ============================================================

st.title("🧠 Python & Deep Learning Assessment")

TOTAL_QUESTIONS = len(QUESTIONS)

st.caption(
    f"{TOTAL_QUESTIONS} MCQs • Medium Level • "
    f"90 Minutes • 1 Mark Each"
)


# ============================================================
# START SCREEN
# ============================================================

if st.session_state.screen == "start":

    name = st.text_input(
        "Student Name",
        placeholder="Enter full name"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Questions",
        TOTAL_QUESTIONS
    )

    c2.metric(
        "Time",
        "90 min"
    )

    c3.metric(
        "Marks",
        TOTAL_QUESTIONS
    )

    c4.metric(
        "Pass",
        f"{PASS_PERCENT}%"
    )

    st.info(
        "Python • NumPy • Pandas • "
        "Deep Learning • CNN • Model Training"
    )

    if st.button(
        "🚀 Start Quiz",
        type="primary",
        use_container_width=True
    ):

        if name.strip():

            start_quiz(name)

            st.rerun()

        else:

            st.error(
                "Please enter the student's name."
            )


# ============================================================
# QUIZ SCREEN
# ============================================================

elif st.session_state.screen == "quiz":

    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------

    elapsed = int(
        time.time() -
        st.session_state.start_time
    )

    remaining = max(
        0,
        TIME_LIMIT - elapsed
    )

    # Automatically submit when time expires.
    if remaining <= 0:

        finish()

        st.rerun()

    minutes, seconds = divmod(
        remaining,
        60
    )

    st.warning(
        f"⏱️ Time Remaining: "
        f"{minutes:02d}:{seconds:02d}"
    )

    st.progress(
        1 - remaining / TIME_LIMIT
    )

    total = len(
        st.session_state.questions
    )

    answered = len(
        st.session_state.answers
    )

    st.write(
        f"**Student:** {st.session_state.name} | "
        f"**Answered:** {answered}/{total}"
    )

    # --------------------------------------------------------
    # QUIZ FORM
    # --------------------------------------------------------

    with st.form("quiz"):

        for i, q in enumerate(
            st.session_state.questions
        ):

            st.markdown(
                f"### Q{i + 1}. {q['q']}"
            )

            # ------------------------------------------------
            # IMPORTANT FIX
            # ------------------------------------------------
            #
            # We use a placeholder option.
            # This prevents .index() from receiving an
            # invalid / None value.
            # ------------------------------------------------

            placeholder = "-- Select an answer --"

            radio_options = [
                placeholder
            ] + q["opts"]

            previous_answer = (
                st.session_state.answers.get(i)
            )

            # Validate previous answer.
            if (
                previous_answer is not None
                and isinstance(previous_answer, int)
                and 0 <= previous_answer < len(q["opts"])
            ):

                default_index = previous_answer + 1

            else:

                default_index = 0

            selected = st.radio(
                "Select one:",
                radio_options,
                index=default_index,
                key=f"q{i}"
            )

            # ------------------------------------------------
            # SAFELY STORE ANSWER
            # ------------------------------------------------

            if selected != placeholder:

                # Find selected option safely.
                selected_index = q["opts"].index(
                    selected
                )

                st.session_state.answers[i] = (
                    selected_index
                )

            else:

                # Remove answer if placeholder is selected.
                st.session_state.answers.pop(
                    i,
                    None
                )

            st.caption(
                f"Topic: {q['topic']}"
            )

            st.divider()

        submit = st.form_submit_button(
            "✅ Submit Quiz",
            type="primary",
            use_container_width=True
        )

    # --------------------------------------------------------
    # SUBMIT
    # --------------------------------------------------------

    if submit:

        unanswered = [
            i + 1
            for i in range(
                len(st.session_state.questions)
            )
            if i not in st.session_state.answers
        ]

        if unanswered:

            display_unanswered = ", ".join(
                map(str, unanswered)
            )

            st.error(
                f"Please answer all {total} questions. "
                f"Unanswered questions: "
                f"{display_unanswered}"
            )

        else:

            finish()

            st.rerun()


# ============================================================
# RESULT SCREEN
# ============================================================

else:

    score = st.session_state.score

    total = len(
        st.session_state.questions
    )

    pct = (
        score / total * 100
        if total
        else 0
    )

    st.success(
        "Quiz submitted successfully!"
    )

    st.header(
        f"Result — {st.session_state.name}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Score",
        f"{score}/{total}"
    )

    c2.metric(
        "Percentage",
        f"{pct:.1f}%"
    )

    c3.metric(
        "Grade",
        grade_for(pct)
    )

    if pct >= PASS_PERCENT:

        st.success("PASS")

    else:

        st.error("FAIL")

    # --------------------------------------------------------
    # SAVE STATUS
    # --------------------------------------------------------

    if st.session_state.get("save_ok"):

        st.success(
            st.session_state.save_msg
        )

    else:

        st.warning(
            st.session_state.get(
                "save_msg",
                "Google Sheets not configured."
            )
        )

    # --------------------------------------------------------
    # TOPIC PERFORMANCE
    # --------------------------------------------------------

    st.subheader(
        "📚 Topic-wise Performance"
    )

    topics = {}

    for i, q in enumerate(
        st.session_state.questions
    ):

        topic = q["topic"]

        if topic not in topics:

            topics[topic] = [0, 0]

        topics[topic][1] += 1

        if (
            st.session_state.answers.get(i)
            == q["a"]
        ):

            topics[topic][0] += 1

    for topic, (
        correct,
        topic_total
    ) in topics.items():

        percentage = (
            correct / topic_total * 100
            if topic_total
            else 0
        )

        st.write(
            f"**{topic}: "
            f"{correct}/{topic_total} "
            f"({percentage:.1f}%)**"
        )

        st.progress(
            correct / topic_total
            if topic_total
            else 0
        )

    st.info(
        "Correct answers are hidden from students. "
        "Teachers can review results from the "
        "Teacher Dashboard."
    )

    # --------------------------------------------------------
    # NEW ATTEMPT
    # --------------------------------------------------------

    if st.button(
        "🔄 New Attempt",
        type="primary",
        use_container_width=True
    ):

        # Clear quiz-related state.
        for key in list(
            st.session_state.keys()
        ):

            del st.session_state[key]

        st.rerun()
