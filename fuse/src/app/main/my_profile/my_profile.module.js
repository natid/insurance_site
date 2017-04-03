(function ()
{
    'use strict';

    angular
        .module('app.my_profile', [])
        .config(config);

    /** @ngInject */
    function config($stateProvider, $translatePartialLoaderProvider, msApiProvider, msNavigationServiceProvider)
    {
        // State
        $stateProvider
            .state('app.my_profile', {
                url    : '/my_profile',
                views  : {
                    'content@app': {
                        templateUrl: 'app/main/my_profile/my_profile.html',
                        controller : 'MyProfileController as vm'
                    }
                }
            });

        // Navigation
        msNavigationServiceProvider.saveItem('personal', {
            title : 'האיזור האישי',
            group : true,
            weight: 2
        });

        msNavigationServiceProvider.saveItem('personal.profile', {
            title    : 'Profile',
            icon     : 'icon-account',
            state    : 'app.my_profile',
            /*stateParams: {
                'param1': 'page'
             },*/
            translate: 'PROFILE.TITLE',
            weight   : 1
        });

        // Translation
        $translatePartialLoaderProvider.addPart('app/main/my_profile');

    }

})();