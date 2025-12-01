import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage for multiple warehouses
warehouses = {}
warehouse_counter = 0


@app.route('/')
def index():
    """Home page showing all warehouses"""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse"""
    if request.method == 'POST':
        global warehouse_counter
        name = request.form.get('name', '').strip()
        
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
        except (ValueError, TypeError):
            flash('Invalid numeric input! Please enter valid numbers.', 'error')
            return redirect(url_for('create_warehouse'))
        
        if not name:
            flash('Warehouse name is required!', 'error')
            return redirect(url_for('create_warehouse'))
        
        if tilavuus <= 0:
            flash('Capacity must be greater than 0!', 'error')
            return redirect(url_for('create_warehouse'))
        
        warehouse_counter += 1
        warehouse_id = warehouse_counter
        warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        
        flash(f'Warehouse "{name}" created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View warehouse details"""
    if warehouse_id not in warehouses:
        flash('Warehouse not found!', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    return render_template('warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit warehouse properties"""
    if warehouse_id not in warehouses:
        flash('Warehouse not found!', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
        except (ValueError, TypeError):
            flash('Invalid numeric input! Please enter a valid number.', 'error')
            return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))
        
        if not name:
            flash('Warehouse name is required!', 'error')
            return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))
        
        if tilavuus <= 0:
            flash('Capacity must be greater than 0!', 'error')
            return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))
        
        # Update name
        warehouse['name'] = name
        
        # Update capacity if different
        old_varasto = warehouse['varasto']
        if old_varasto.tilavuus != tilavuus:
            # Create new Varasto with updated capacity, preserving saldo if possible
            new_saldo = min(old_varasto.saldo, tilavuus)
            warehouse['varasto'] = Varasto(tilavuus, new_saldo)
        
        flash(f'Warehouse "{name}" updated successfully!', 'success')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    return render_template('edit.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add items to warehouse"""
    if warehouse_id not in warehouses:
        flash('Warehouse not found!', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    try:
        maara = float(request.form.get('maara', 0))
    except (ValueError, TypeError):
        flash('Invalid numeric input! Please enter a valid number.', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    if maara <= 0:
        flash('Amount must be greater than 0!', 'error')
    else:
        warehouse['varasto'].lisaa_varastoon(maara)
        flash(f'Added {maara} units to warehouse "{warehouse["name"]}"!', 'success')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove items from warehouse"""
    if warehouse_id not in warehouses:
        flash('Warehouse not found!', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    try:
        maara = float(request.form.get('maara', 0))
    except (ValueError, TypeError):
        flash('Invalid numeric input! Please enter a valid number.', 'error')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    
    if maara <= 0:
        flash('Amount must be greater than 0!', 'error')
    else:
        otettu = warehouse['varasto'].ota_varastosta(maara)
        flash(f'Removed {otettu} units from warehouse "{warehouse["name"]}"!', 'success')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete warehouse entirely"""
    if warehouse_id not in warehouses:
        flash('Warehouse not found!', 'error')
        return redirect(url_for('index'))
    
    warehouse_name = warehouses[warehouse_id]['name']
    del warehouses[warehouse_id]
    flash(f'Warehouse "{warehouse_name}" deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
