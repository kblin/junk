import os
import logging
import inspect


def trace_caller(prefix, filter_from=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            frame_obj, orig_filename, line_no, sfunc, line_content, _ = inspect.stack()[1]
            filename = os.sep.join(orig_filename.split(os.sep)[-2:])
            # This way we catch .py or .pyc
            if not filter_from or not filter_from.startswith(orig_filename):
                logging.debug("%s:%s:%s:%r\n%s" % (prefix, filename, line_no, sfunc, line_content[0]))
            return func(*args, **kwargs)
        return new_func
    return decorator


class TraceList(list):
    @trace_caller('TLINI')
    def __init__(self, *args):
        return super(TraceList, self).__init__(*args)

    @trace_caller('TLSET')
    def __setitem__(self, item, value):
        return super(TraceList, self).__setitem__(item, value)

    @trace_caller('TLGET')
    def __getitem__(self, item):
        return super(TraceList, self).__getitem__(item)

    @trace_caller('TLADD')
    def append(self, item):
        return super(TraceList, self).append(item)


class TraceDict(dict):
    @trace_caller('TDINI')
    def __init__(self, *args):
        return super(TraceDict, self).__init__(*args)

    @trace_caller('TDSET')
    def __setitem__(self, item, value):
        return super(TraceDict, self).__setitem__(item, value)

    @trace_caller('TDGET')
    def __getitem__(self, item):
        return super(TraceDict, self).__getitem__(item)

