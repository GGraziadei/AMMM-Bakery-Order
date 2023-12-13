/*********************************************
 * OPL 22.1.1.0 Model
 * Author: Gianluca Graziadei
 * Creation Date: 7 dic 2023 at 19:50:41
 *********************************************/

 main {
        
    for(var instance = 0; instance<5; instance+=1){
    
	    var src = new IloOplModelSource("model_a_improved.mod");
	    var def = new IloOplModelDefinition(src);
	    var cplex = new IloCplex();
	    var model = new IloOplModel(def,cplex);
	    
      	var data_file = "benchmark/" + instance + ".dat";
      	
        var data = new IloOplDataSource(data_file);
	    model.addDataSource(data);
	    model.generate();
	    
	    var start, end, elapsed;
	    writeln("Instance: " + data_file);
	    start = cplex.getDetTime();
	    if (cplex.solve()) {
	      	end = cplex.getDetTime();
	      	elapsed = end - start;
	      	
	        writeln("Obj.value: " + cplex.getObjValue() );
	        writeln("Elapsed time: " + elapsed);
	    }
	    else {
	        writeln("Not feasible.");
	    }
	    
	    model.end();
	    data.end();
	    def.end();
	    cplex.end();
	    src.end();
   }
};