import datetime

from anki import stats
from anki.hooks import wrap
from anki.stats import *

import graph


def chunkingFilter(self):
    if self.type == 0:
        # days (in 1 month)
        chunk, chunksize = 30, 1
    elif self.type == 1:
        # weeks (in 1 year)
        chunk, chunksize = 52, 7
    else:
        # months (in indefinite)
        chunk, chunksize = None, 30

    return chunk, chunksize


def history(data, chunks=None, chunk_size=1):
    if not chunks:
        try:
            chunks = int(max([row[0] for row in data])) / chunk_size + 1  # nb of periods to look back
        except:
            chunks = 1  # This happens if the deck contains no Chinese
    histogram = [[] for x in range(chunks + 1)]
    delta = []
    date = -chunks
    # Fill histogram, as a list. d = nb of days in the past (0=today).
    for day, HSKLevel in data:
        if day <= chunks * chunk_size:  # TODO: use filtering
            histogram[day / chunk_size].append(HSKLevel)
    # Fill history, as a list of coordinates: [(relative_day, nb_values),...]
    while len(histogram):
        v = histogram.pop()
        delta.append((date, v))
        date += 1
    return delta


def get_data(self):
    return self.col.db.all('SELECT revlog.id, notes.sfld FROM revlog, notes, cards WHERE revlog.type=1 AND '
                           'revlog.cid = '
                           'cards.id AND cards.nid = notes.id GROUP BY notes.id ORDER BY revlog.id ')


def set_Relative_Time(data):
    # Minus the stored time from the current time to get how many days since
    now = datetime.datetime.now()
    return [((now - datetime.datetime.fromtimestamp(row[0] * 0.001)).days, row[1]) for row in data]


def process_Graph_Data(data, graphFunc, graphType):
    processedHanziList = graph.processHanzi(data, graphFunc, graphType)
    return processedHanziList


def make_graph(self, data):
    graphColumnColours = ['#A00041', '#D73C4C', '#F66D3A', '#FFAF59', '#FFE185', '#FFFFBC', '#ECEBCA']

    txt = self._title(_("HSK level"),
                      _("Words learnt by HSK level"))
    data = [dict(data=[(day, level[item - 1]) for day, level in data], color=graphColumnColours[item - 1], yaxis=1, \
                 label=_(("HSK" + str(
                     item) if item < 7 else "Non-HSK")),
                 bars={'show': False}, lines={"show": True, "lineWidth": 0, "fill": 0.8}) for item in range(1, 8)]
    txt += self._graph(id="hsk", data=data, conf=dict(xaxis=dict(tickDecimals=0), yaxis=dict(autoscaleMargin=0.1)))
    return txt


def build_graph(self, graphType):
    data = get_data(self)
    data = set_Relative_Time(data)
    chunk, chunksize = chunkingFilter(self)

    new_data = process_Graph_Data(data, graph.graphProfiles[graphType]['countingFunctions'], 'HSK')
    chunked_data = history(new_data, chunk, chunksize)
    combined_data = countHSKLevels(chunked_data)
    gra = make_graph(self, combined_data)
    return gra


def countHSKLevels(data):
    levels = [0] * 7
    running_total_data = []
    for idx, values in enumerate(data):
        day, level_count = values
        running_total_data.append([day, []])
        for level in range(1, 8):
            levels[level - 1] += level_count.count(level)
            running_total_data[idx][-1].append(levels[level - 1])
    return running_total_data



def my_report(self, _old):
    # 0=days, 1=weeks, 2=months

    oldreturn = _old(self)
    self.type = self.type | 0
    txt = build_graph(self, 'HSK')

    return oldreturn + "<script>%s\n</script><center>%s</center>" % (
        anki.js.jquery + anki.js.plot, txt)


stats.CollectionStats.todayStats = wrap(stats.CollectionStats.todayStats, my_report, "around")
