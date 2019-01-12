class Executer:
    _runners = {}

    def register_runner(self, cls_):
        try:
            languages = cls_.supported_languages
            for lang in languages:
                if lang not in self._runners:
                    print "REGISTER:{}, language:{}".format(cls_, lang)
                    self._runners[lang] = cls_
        except Exception, e:
            print e.message

    def find_runner(self, language):
        return self._runners[language]

    def get_supported_languages(self):
        return self._runners.keys()

    def execute_snippet(self, function_signature, code_snippet):
        runner = self.find_runner(code_snippet.language)
        return runner.execute_snippet(function_signature, code_snippet)

    def execute_code(self, language, return_type, code):
        runner = self.find_runner(language)
        return runner.execute_code(return_type, code)


executor = Executer()


class Registrator(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = type.__new__(cls, clsname, bases, attrs)
        executor.register_runner(newclass)
        return newclass