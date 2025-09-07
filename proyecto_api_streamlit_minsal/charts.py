
import matplotlib.pyplot as plt

def bar_top(df, cat_col: str, val_col: str, title: str):
    fig, ax = plt.subplots()
    plot_df = df.sort_values(val_col, ascending=True)
    ax.barh(plot_df[cat_col].astype(str), plot_df[val_col])
    ax.set_title(title)
    ax.set_xlabel(val_col)
    ax.set_ylabel(cat_col)
    return fig

def line_by_date(df, date_col: str, title: str):
    fig, ax = plt.subplots()
    plot_df = df.dropna(subset=[date_col]).copy()
    plot_df[date_col] = plot_df[date_col].astype('datetime64[ns]')
    s = plot_df.groupby(plot_df[date_col].dt.date).size()
    ax.plot(s.index, s.values)
    ax.set_title(title)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Conteo')
    fig.autofmt_xdate()
    return fig
