(function ()
{
    'use strict';

    angular
        .module('fuse')
        .config(config);

    /** @ngInject */
    function config($stateProvider, $translatePartialLoaderProvider, msNavigationServiceProvider)
    {
        // State
        $stateProvider
            .state('login', {
                url    : '/login',
                views  : {
                    'main@': {
                        templateUrl: 'app/main/login/login.html',
                        controller : 'LoginController as vm'
                    },
                       'toolbar@app'   : {
                           template:'',
                    },
                    'navigation@app': {
                        template:'',
                    },
                    'quickPanel@app': {
                        template:'',
                    }
                }
            });

    }
})();