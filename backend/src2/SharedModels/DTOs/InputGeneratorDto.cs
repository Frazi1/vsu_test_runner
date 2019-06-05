using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class InputGeneratorDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string CreatedByUser { get; set; }
        public List<GeneratorCallArgumentDto> CallArguments { get; set; }
        public CodeSnippetDto CodeSnippet { get; set; }        
    }
}