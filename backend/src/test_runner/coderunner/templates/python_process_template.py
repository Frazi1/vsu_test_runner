def __notify_iteration():
    def wrapper(fn):
        def _inner(*a, **kwa):
            print("<StartIteration>")
            fn(*a, **kwa)
            print("<EndIteration>")

        return _inner

    return wrapper


def run():
    %FUNC_DECLARATION%

    %FUNC_CALL%

run()
