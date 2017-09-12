/**
 * :copyright (c) 2014 - 2017, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.
 * :author
 */
angular.module('BE.seed.controller.matching_detail_settings', [])
  .controller('matching_detail_settings_controller', [
    '$scope',
    '$window',
    '$uibModalInstance',
    '$stateParams',
    'inventory_service',
    'user_service',
    'columns',
    function ($scope, $window, $uibModalInstance, $stateParams, inventory_service, user_service, columns) {
      $scope.inventory_type = $stateParams.inventory_type;
      $scope.inventory = {
        id: $stateParams.inventory_id
      };
      $scope.cycle = {
        id: $stateParams.cycle_id
      };

      var localStorageKey = 'grid.' + $scope.inventory_type + '.detail';

      var restoreDefaults = function () {
        inventory_service.removeSettings(localStorageKey);
        $scope.data = inventory_service.loadSettings(localStorageKey, columns);
        _.defer(function () {
          // Set row selection
          $scope.gridApi.selection.clearSelectedRows();
          _.forEach($scope.gridApi.grid.rows, function (row) {
            if (row.entity.visible === false) row.setSelected(false);
            else row.setSelected(true);
          });
        });
      };

      var saveSettings = function () {
        $scope.data = inventory_service.reorderSettings($scope.data);
        inventory_service.saveSettings(localStorageKey, $scope.data);
      };

      var rowSelectionChanged = function () {
        _.forEach($scope.gridApi.grid.rows, function (row) {
          row.entity.visible = row.isSelected;
        });
        saveSettings();
      };

      $scope.updateHeight = function () {
        var height = 0;
        _.forEach(['.header', '.page_header_container', '.section_nav_container', '.section_header_container', '.section_content.with_padding'], function (selector) {
          var element = angular.element(selector)[0];
          if (element) height += element.offsetHeight;
        });
        angular.element('#grid-container').css('height', 'calc(100vh - ' + (height + 2) + 'px)');
        angular.element('#grid-container > div').css('height', 'calc(100vh - ' + (height + 4) + 'px)');
        $scope.gridApi.core.handleWindowResize();
      };

      $scope.data = inventory_service.loadSettings(localStorageKey, columns);

      $scope.gridOptions = {
        data: 'data',
        enableColumnMenus: false,
        enableFiltering: true,
        enableGridMenu: true,
        enableSorting: false,
        gridMenuCustomItems: [{
          title: 'Reset defaults',
          action: restoreDefaults
        }],
        gridMenuShowHideColumns: false,
        minRowsToShow: 30,
        rowTemplate: '<div grid="grid" class="ui-grid-draggable-row" draggable="true"><div ng-repeat="(colRenderIndex, col) in colContainer.renderedColumns track by col.colDef.name" class="ui-grid-cell" ng-class="{ \'ui-grid-row-header-cell\': col.isRowHeader, \'custom\': true }" ui-grid-cell></div></div>',
        columnDefs: [{
          name: 'displayName',
          displayName: 'Column Name',
          enableHiding: false
        }],
        onRegisterApi: function (gridApi) {
          $scope.gridApi = gridApi;
          _.defer(function () {
            // Set row selection
            _.forEach($scope.gridApi.grid.rows, function (row) {
              if (row.entity.visible === false) row.setSelected(false);
              else row.setSelected(true);
            });
          });

          gridApi.selection.on.rowSelectionChanged($scope, rowSelectionChanged);
          gridApi.selection.on.rowSelectionChangedBatch($scope, rowSelectionChanged);
          gridApi.draggableRows.on.rowDropped($scope, saveSettings);

          _.delay($scope.updateHeight, 150);
          var debouncedHeightUpdate = _.debounce($scope.updateHeight, 150);
          angular.element($window).on('resize', debouncedHeightUpdate);
          $scope.$on('$destroy', function () {
            angular.element($window).off('resize', debouncedHeightUpdate);
          });
        }
      };
    }]);
