odoo.define('asian_quotation.list_editable_renderer', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');

    ListRenderer.include({

        _extractEvenRowColorAttrs: function (arch) {
            let even_number_color = {};
            for (const [key, expr] of Object.entries(arch.attrs)) {
                if (key === 'even-row-color') {
                    even_number_color = py.parse(py.tokenize(expr));
                }
            }
            return even_number_color;
        },

        _setEvenRowColor: function (even_number_color, record, $tr) {
            $tr.toggleClass('even-row-color', py.PY_isTrue(py.evaluate(even_number_color, record.evalContext)));
        },

        _renderRow: function (record, index) {
            var $row = this._super.apply(this, arguments);
            if (this.mode !== 'edit' && this.state.groupedBy.length === 0){
                let index = this.state.data.findIndex(function(e){return record.id===e.id})
                let even_number_color = this._extractEvenRowColorAttrs(this.arch);
                if (index !== -1 && Object.keys(even_number_color).length > 0 && index % 2 === 0){
                    this._setEvenRowColor(even_number_color, record, $row)
                }
            }
            return $row;
        },

    });
});