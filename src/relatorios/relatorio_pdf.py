from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import numpy


def format_data(title, header, firstcolumn, values):
    titleLine = []
    titleLine.append(title)
    for i in range(len(header)-1):
        titleLine.append('')

    data = [titleLine, header]

    import locale
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

    for row in values:
        data.append([locale.currency(v) for v in row])

    if(len(firstcolumn) > 0):
        firstcolumn.insert(0, title)
        print(firstcolumn)
        print(data)
        aux = numpy.array(data)
        data = numpy.insert(aux, 0, firstcolumn, axis=1).tolist()

    return data


def generate_table(title, header, firstcolumn, values):
    tStyle = TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # cabecalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('BACKGROUND', (0, 1), (-1, 1), colors.darkgray),
        # valores
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ])

    # Loop through list of lists creating styles for cells with negative value.
    for row, elements, in enumerate(values):
        for column, value in enumerate(elements):
            if value < 0:
                tStyle.add('TEXTCOLOR', (column+1, row+2),
                           (column+1, row+2), colors.red)

    data = format_data(title, header, firstcolumn, values)

    t = Table(data, len(data[0])*[1.2*inch], len(data)*[0.16*inch])
    t.setStyle(tStyle)

    return t


def addSpace(elements):
    # Adding space between two tables
    from reportlab.platypus import Table
    t = Table([['\n']])
    elements.append(t)


def add_legend(draw_obj, chart, data):
    from reportlab.graphics.charts.legends import Legend
    from reportlab.lib.validators import Auto
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


def generate_graph(detalhamento, month, filename):
    print(" - Creating graph: ")

    import matplotlib.pylab as plt

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    meses = []
    for i in range(1, 13):
        meses.append(i)

    for categoria in detalhamento:
        #plt.plot(scurves[strategy], config_generator.symbols[strategy], color=config_generator.colors[strategy], markevery=marks, label=config_generator.abbreviations[strategy])
        plt.plot(meses[0:month], detalhamento[categoria]
                 [0:month], label=categoria, markevery=1.0)

    plt.ylabel('Receita')
    plt.xticks(meses[0:month])  # hide axis x
    plt.legend()  # show line names
    plt.savefig('img/'+filename+'.png', format='png')
