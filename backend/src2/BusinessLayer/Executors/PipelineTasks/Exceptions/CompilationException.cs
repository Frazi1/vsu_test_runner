using System;

namespace BusinessLayer.Executors.PipelineTasks.Exceptions
{
    public class CompilationException: Exception
    {
        public CompilationException(string message) : base(message)
        {
        }
    }
}