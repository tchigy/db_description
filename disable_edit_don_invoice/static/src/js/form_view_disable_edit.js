openerp.disable_edit_don_invoice = function(instance, local) {
    var instance = openerp;
    var FormView = instance.web.FormView;

    // override load_record
    FormView.include({
        load_record: function(record) {
        // disable only for account.invoice
        if (record){
            if (this.model == 'account.invoice' & _.contains(['paid', 'cancel'], record.state)){
                    $('button.oe_form_button_edit').hide()
                }else {
                    $('button.oe_form_button_edit').show()
                }
        }
        // call super
        return this._super(record);
        }
    });
}