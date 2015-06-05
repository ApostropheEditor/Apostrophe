describe('Core_populateFromArray', function () {
  var id = 'testContainer';

  beforeEach(function () {
    this.$container = $('<div id="' + id + '"></div>').appendTo('body');
  });

  afterEach(function () {
    if (this.$container) {
      destroy();
      this.$container.remove();
    }
  });

  var arrayOfArrays = function () {
    return [
      ["", "Kia", "Nissan", "Toyota", "Honda", "Mix"],
      ["2008", 10, 11, 12, 13, {a: 1, b: 2}],
      ["2009", 20, 11, 14, 13, {a: 1, b: 2}],
      ["2010", 30, 15, 12, 13, {a: 1, b: 2}]
    ];
  };

  it('should call onChange callback', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      }
    });
    populateFromArray(0, 0, [["test","test"],["test","test"]], 1, 1);

    expect(output).toEqual([[0,0,'','test'],[0,1,'Kia','test'],[1,0,'2008','test'],[1,1,10,'test']]);
  });

  it('should populate single value for whole selection', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      }
    });
    populateFromArray(0, 0, [["test"]], 3, 0);

    expect(output).toEqual([[0,0,'','test'],[1,0,'2008','test'],[2,0,'2009','test'],[3,0,'2010','test']]);
  });

  it('should populate value for whole selection only if populated data isn\'t an array', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      }
    });
    populateFromArray(0, 0, [['test'], [[1, 2, 3]]], 3, 0);

    expect(output).toEqual([[0, 0, '', 'test' ], [2, 0, '2009', 'test']]);
  });

  it('should populate value for whole selection only if populated data isn\'t an object', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      }
    });
    populateFromArray(0, 0, [['test'], [{test: 1}]], 3, 0);

    expect(output).toEqual([[0, 0, '', 'test' ], [2, 0, '2009', 'test']]);
  });

  it('shouldn\'t populate value if original value doesn\'t have the same data structure', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      }
    });
    populateFromArray(1, 3, [['test']], 1, 5);

    expect(output).toEqual([[1, 3, 12, 'test' ], [1, 4, 13, 'test']]);
  });

  it('should shift values down', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      },
      minSpareRows: 1
    });
    populateFromArray(0, 0, [["test","test2"],["test3","test4"]], 2, 2, null, 'shift_down');

    expect(getData()).toEqual([
      ["test", "test2", "test", "Toyota", "Honda", "Mix"],
      ["test3", "test4", "test3", 12, 13, { a : 1, b : 2 }],
      ["test", "test2", "test", 14, 13, { a : 1, b : 2 }],
      ["", "Kia", "Nissan", 12, 13, { a : 1, b : 2 }],
      ["2008", 10, 11, null, null, null],
      ["2009", 20, 11, null, null, null],
      ["2010", 30, 15, null, null, null],
      [null, null, null, null, null, null]
    ]);
  });

  it('should shift values right', function () {
    var output = null;

    handsontable({
      data : arrayOfArrays(),
      afterChange: function (changes) {
        output = changes;
      },
      minSpareCols: 1
    });
    populateFromArray(0, 0, [["test","test2"],["test3","test4"]], 2, 2, null, 'shift_right');

    expect(getData()).toEqual([
      ["test", "test2", "test", "", "Kia", "Nissan", "Toyota", "Honda", "Mix", null],
      ["test3", "test4", "test3", "2008", 10, {a: 1, b: 2}, 12, 13, null, null],
      ["test", "test2", "test", "2009", 20, {a: 1, b: 2}, 14, 13, null, null],
      ["2010", 30, 15, 12, 13, {a: 1, b: 2}, null, null, null, null]
    ]);
  });

  it('should run beforeAutofillInsidePopulate hook for each inserted value', function () {
    var called = 0;

    var hot = handsontable({
      data : arrayOfArrays()
    });

    hot.addHook('beforeAutofillInsidePopulate', function (index) {
      called++;
    });

    populateFromArray(0, 0, [["test","test2"],["test3","test4"]], 1, 1, 'autofill', 'overwrite');

    expect(called).toEqual(4);
  });

  it('should run beforeAutofillInsidePopulate hook and could change cell data before insert if returned object with value property', function () {

    var hot = handsontable({
      data : arrayOfArrays()
    });

    hot.addHook('beforeAutofillInsidePopulate', function (index) {
      return {
        value: 'my_test'
      };
    });

    populateFromArray(0, 0, [["test","test2"],["test3","test4"]], 1, 1, 'autofill', 'overwrite');

    expect(getDataAtCell(0,0)).toEqual('my_test');
  });
});
