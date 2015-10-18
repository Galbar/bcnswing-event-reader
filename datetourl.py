import re
import datetime

def datetourl(date_string):

    m = re.match('^(?:((?:\d{1,2}[-/]){2}\d{2,4})|(:?(?:[Pp]roximo )?(\w+)))$', date_string)
    error = False

    if m is None:
        error = True

    elif m.group(1) is not None:
        l = map(lambda x: int(x), re.split('[-/]', date_string))

        try:
            date = datetime.date(year=l[2], month=l[1], day=l[0])
        except ValueError:
            error = True

    else:
        weekdays = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
        day_name = m.group(2).lower()
        today = datetime.date.today()
        try:
            weekday_num = weekdays.index(day_name)
            days_delta = (weekday_num - today.weekday()) % 7
            date = today + datetime.timedelta(days=days_delta)
        except ValueError:
            error = True

    if error or datetime.date.today() > date:
        attr = ''
    else:
        attr = '&year=%i&month=%i&day=%i' % (date.year, date.month, date.day)

    return 'http://bcnswing.org/swing/index.php?option=com_jevents&task=day.listevents&lang=ca' + attr

if __name__ == '__main__':
    import sys
    print datetourl(sys.argv[1])
