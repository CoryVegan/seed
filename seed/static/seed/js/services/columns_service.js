/**
 * :copyright (c) 2014 - 2019, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.
 * :author
 */
angular.module('BE.seed.service.columns', []).factory('columns_service', [
  '$http',
  'user_service',
  function ($http, user_service) {

    var columns_service = {};

    columns_service.patch_column = function (column_id, data) {
      return columns_service.patch_column_for_org(user_service.get_organization().id, column_id, data);
    };

    columns_service.patch_column_for_org = function (org_id, column_id, data) {
      return $http.patch('/api/v2/columns/' + column_id + '/', data, {
        params: {
          organization_id: org_id
        }
      }).then(function (response) {
        return response.data;
      });
    };

    return columns_service;

  }]);
