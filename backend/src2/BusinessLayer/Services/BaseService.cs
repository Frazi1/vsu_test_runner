using System;
using BusinessLayer.Authentication;

namespace BusinessLayer.Services
{
    public abstract class BaseService
    {
        private readonly Func<ICurrentUser> _getCurrentUser;
        
        private ICurrentUser _currentUser;
        protected ICurrentUser CurrentUser => _currentUser ?? (_currentUser = _getCurrentUser());

        protected BaseService(Func<ICurrentUser> currentUser)
        {
            _getCurrentUser = currentUser;
        }

        protected BaseService(ICurrentUser currentUser)
        {
            _currentUser = currentUser;
        }
    }
}