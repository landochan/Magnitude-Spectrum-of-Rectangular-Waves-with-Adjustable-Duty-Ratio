import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.widgets import Slider, Button


# Constants
TIME_REGION = 'Time Region'
FREQUENCY_REGION = 'Frequency Region'
DPI = 185
TIME_CYCLE_N = 10
FREQ_N = 20
INIT_DUTY_RATIO = 0.5
temp_time_y_arr = np.array([0, 1, 1, 0]*(2*TIME_CYCLE_N))
INIT_TIME_Y_ARR = np.concatenate((temp_time_y_arr, [0]))


# Plt parameters setting
plt.rcParams.update({'font.size': 7})
plt.rcParams['toolbar'] = 'None'


def get_data_time(duty_ratio):
    # Returns x and y arrays for time region plotting
    x_arr = np.array([-TIME_CYCLE_N, TIME_CYCLE_N])

    if duty_ratio == 1:
        y_arr = np.ones(2)
        return x_arr, y_arr

    elif duty_ratio == 0:
        y_arr = np.zeros(2)
        return x_arr, y_arr

    temp_x_arr = np.arange(-TIME_CYCLE_N, TIME_CYCLE_N, 1)
    temp_x_arr = np.concatenate((temp_x_arr, temp_x_arr + duty_ratio))
    temp_x_arr = np.concatenate((temp_x_arr, temp_x_arr))
    temp_x_arr = np.sort(temp_x_arr)
    x_arr = np.append(temp_x_arr, [TIME_CYCLE_N])

    y_arr = INIT_TIME_Y_ARR

    return x_arr, y_arr


def get_data_frequency(duty_ratio):
    # Returns x and y arrays for frequency region stem plotting
    x_arr = np.arange(FREQ_N+1)
    y_arr = np.zeros(FREQ_N+1)
    y_arr[0] = duty_ratio

    if duty_ratio == 0 or duty_ratio == 1:
        return x_arr, y_arr

    y_arr[1:] = np.abs(2 * np.sin(np.pi * duty_ratio * x_arr[1:])/(np.pi * x_arr[1:]))

    return x_arr, np.around(y_arr, 3)


# Creates figure and axes settings
fig, axes = plt.subplot_mosaic([[TIME_REGION, FREQUENCY_REGION]],
                               figsize=(5, 3), dpi=DPI,
                               facecolor='lightskyblue', layout='constrained')
# fig.suptitle('Magnitude Spectrum of Rectangular Waves with Adjustable Duty Ratio', y=0.96, fontweight='bold')
fig.canvas.manager.set_window_title('Magnitude Spectrum of Rectangular Waves with Adjustable Duty Ratio')

axes[TIME_REGION].set_title(TIME_REGION)
axes[TIME_REGION].set_xlabel('Time (T)')
axes[TIME_REGION].set_ylabel('Voltage (Vmax)')
axes[TIME_REGION].grid(True)
axes[TIME_REGION].set_position([0.15, 0.4, 0.3, 0.5])
axes[TIME_REGION].set_xlim((-1.1, 1.1))
axes[TIME_REGION].set_ylim((-0.05, 1.05))
# axes[TIME_REGION].yaxis.set_major_locator(ticker.MultipleLocator(1))

axes[FREQUENCY_REGION].set_title(FREQUENCY_REGION)
axes[FREQUENCY_REGION].set_xlabel('Frequency (1/T)')
axes[FREQUENCY_REGION].set_ylabel('Voltage (Vmax)')
axes[FREQUENCY_REGION].set_ylim((-0.05, 1.05))
axes[FREQUENCY_REGION].grid(False)
axes[FREQUENCY_REGION].set_position([0.63, 0.4, 0.3, 0.5])
axes[FREQUENCY_REGION].xaxis.set_major_locator(ticker.MultipleLocator(2))
# axes[FREQUENCY_REGION].yaxis.set_major_locator(ticker.MultipleLocator(0.1))


# Start plotting
time_x_arr, time_y_arr = get_data_time(INIT_DUTY_RATIO)
time_lines, = axes[TIME_REGION].plot(time_x_arr, time_y_arr, lw=1.25)
freq_x_arr, freq_y_arr = get_data_frequency(INIT_DUTY_RATIO)
markerline, stemlines, baselines = axes[FREQUENCY_REGION].stem(freq_x_arr, freq_y_arr, bottom=0)
plt.setp(stemlines, linewidth = 1)
plt.setp(markerline, markersize = 2)
plt.setp(baselines, linewidth=0.75)
y_text_arr = np.array([])
for i, j in zip(freq_x_arr, freq_y_arr):
    new_y_text = axes[FREQUENCY_REGION].text(i, j+0.025, str(j), ha='center', va='bottom', rotation=90,
                                             fontsize=4)
    new_y_text.set_visible(False)
    y_text_arr = np.append(y_text_arr, new_y_text)


# Options and Adjustables
# Creating Options Axes
# Duty Ratio Slider
ax_duty_ratio = fig.add_axes([0.15, 0.23, 0.3, 0.03])
duty_ratio_slider = Slider(
    ax=ax_duty_ratio,
    label='Duty ratio',
    valmin=0.0,
    valmax=1.0,
    valinit=INIT_DUTY_RATIO,
    valstep=0.01
)


# Button: reset, show and hide details button
reset_ax = fig.add_axes([0.35, 0.16, 0.1, 0.05])
reset_button = Button(reset_ax, 'Reset', hovercolor='0.975')
show_or_hide_ax = fig.add_axes([0.68, 0.16, 0.2, 0.05])
show_or_hide_button = Button(show_or_hide_ax, 'Show details', hovercolor='0.975')


# Functions
def update_duty_ratio(val):
    time_x_arr, time_y_arr = get_data_time(duty_ratio_slider.val)
    time_lines.set_xdata(time_x_arr)
    time_lines.set_ydata(time_y_arr)

    freq_x_arr, freq_y_arr = get_data_frequency(duty_ratio_slider.val)
    markerline.set_ydata(freq_y_arr)

    stemlines.set_paths([np.array([[xx, 0], [xx, yy]]) for (xx, yy) in zip(freq_x_arr, freq_y_arr)])

    for i in range(FREQ_N+1):
        y_text_arr[i].set_text(str(freq_y_arr[i]))
        y_text_arr[i].set_position((freq_x_arr[i], freq_y_arr[i] + 0.025))

    fig.canvas.draw_idle()


def reset(event):
    duty_ratio_slider.reset()


def show_or_hide(event):
    if y_text_arr[0].get_visible() == True:
        for y_text in y_text_arr:
            y_text.set_visible(False)
        show_or_hide_button.label.set_text('Show details')

    else:
        for y_text in y_text_arr:
            y_text.set_visible(True)
        show_or_hide_button.label.set_text('Hide details')

    fig.canvas.draw()


# Connecting the functions to the slider or button
duty_ratio_slider.on_changed(update_duty_ratio)
reset_button.on_clicked(reset)
show_or_hide_button.on_clicked(show_or_hide)



# Credit text
fig.text(x=0.5, y=0.025, s='© Lando Chan', ha='center', figure=fig)


plt.show()