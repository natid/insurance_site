(function ()
{
    'use strict';

    angular
        .module('fuse')
        .run(runBlock);

    /** @ngInject */
    function runBlock($rootScope, $timeout, $state, $location, $cookies, $http)
    {
        // Activate loading indicator
        var stateChangeStartEvent = $rootScope.$on('$stateChangeStart', function ()
        {
            $rootScope.loadingProgress = true;
        });

        // De-activate loading indicator
        var stateChangeSuccessEvent = $rootScope.$on('$stateChangeSuccess', function ()
        {
            $timeout(function ()
            {
                $rootScope.loadingProgress = false;
            });
        });

        // Store state in the root scope for easy access
        $rootScope.state = $state;

        // Cleanup
        $rootScope.$on('$destroy', function ()
        {
            stateChangeStartEvent();
            stateChangeSuccessEvent();
        });

        // keep user logged in after page refresh
        $rootScope.globals = $cookies.getObject('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata;
        }
 
        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in and trying to access a restricted page
            var restrictedPage = $.inArray($location.path(), ['/login', '/register']) === -1;
            var loggedIn = $rootScope.globals.currentUser;
            $rootScope.loadingProgress = false;
            if (restrictedPage && !loggedIn) {
                $location.path('/login');
            }
        });
    }
})();