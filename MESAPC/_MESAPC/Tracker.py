import matplotlib.pyplot as plt
import MESAPC._MESAPC.data_handler as data_handler



handler = data_handler.DataHandler()

fig, ax = plt.subplots(figsize = (12,8))

handler.load_hists()
colors = ['r', 'b', 'g']
while True:
    run_count = 0
    handler.grid.plot_grid(ax, 'log_Teff', 'log_L')
    ax.plot(ax.set_xlim()[0],ax.set_ylim()[0], 'k-', label ='grid')
    for run in handler.runs:
        run.plot_grid(ax, 'log_Teff', 'log_L', color = colors[run_count])
        ax.plot(ax.set_xlim()[0],ax.set_ylim()[0], f'{colors[run_count]}-', label = run.grid_name)
        run_count += 1
    ax.invert_xaxis()
    ax.set_ylabel('log($L/L_\odot$)')
    ax.set_xlabel('log($T_{\\rm eff}$)')
    ax.legend()
    handler.refresh_files()
    handler.load_hists()
    plt.draw()
    plt.pause(1)
    ax.clear()

