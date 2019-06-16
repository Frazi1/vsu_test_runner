using System.ComponentModel.DataAnnotations.Schema;
using SharedModels.DTOs;

namespace DataAccess.Model
{
    public class DbTestTemplateUserPermission : Permission, IEntityWithId
    {
        public int UserId { get; set; }
        public int TestTemplateId { get; set; }
        
        public virtual DbUser User { get; set; }
        public virtual DbTestTemplate TestTemplate { get; set; }

        [NotMapped]
        public int Id {
            get => UserId;
            set => UserId = value;
        }
    }
}