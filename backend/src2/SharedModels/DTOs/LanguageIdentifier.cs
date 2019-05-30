using JetBrains.Annotations;

namespace SharedModels.DTOs
{
    public class LanguageIdentifier
    {
        public string Id { get; set; }
        public string DisplayName { get; set; }


        [UsedImplicitly]
        private LanguageIdentifier()
        {
        }

        private LanguageIdentifier(string id)
            : this(id, id)
        {
        }

        private LanguageIdentifier(string id, string displayName)
        {
            Id = id;
            DisplayName = displayName;
        }

        public static LanguageIdentifier FromString(string language) => new LanguageIdentifier(language);

        public static LanguageIdentifier FromId(string id, string displayName) =>
            new LanguageIdentifier(id, displayName);


        public static bool operator ==(LanguageIdentifier o1, LanguageIdentifier o2)
        {
            return o1.Equals(o2);
        }

        public static bool operator !=(LanguageIdentifier o1, LanguageIdentifier o2)
        {
            return !(o1 == o2);
        }

        private bool Equals(LanguageIdentifier other)
        {
            return string.Equals(Id, other.Id);
        }

        public override bool Equals(object obj)
        {
            return obj is LanguageIdentifier other && Equals(other);
        }

        public override int GetHashCode()
        {
            return Id != null ? Id.GetHashCode() : 0;
        }

        public override string ToString()
        {
            return Id;
        }
    }
}