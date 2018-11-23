## disable_edit_confirmed_po

Is a module to disable Edit on Purchase Order in state ['done', 'cancel']
You can improve this module by playing around with `form_view_disable_edit.js`
As you can see you can change the condition of the hidden process for example
if you just want to hide edit in confirmed state just change this:

   `if (this.model == 'purchase.order' & _.contains(['done', 'cancel'], record.state))`

   To this:

   `if (this.model == 'purchase.order' & record.state == 'done')`

If you want to have this behavior in other modules like sale.order

    `if (   _.contains(['purchase.order', 'sale.order'], this.model) & _.contains(['done', 'cancel'], record.state))`

    don't forget to add dependency on your addon manifest `__openerp__.py` to make sure that
    your module is installed after sale module
