using SharedModels.Enum;

namespace DataAccess.Model
{
    public class DbUserFeature
    {
        public int UserId { get; set; }
        public FeatureType FeatureType { get; set; }

        public DbUser User { get; set; }
    }
}