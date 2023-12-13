int                    n = ...;    // Number of orders.
int                    t = ...;    // Number of time slots
range                  N = 1..n;   // Range of orders.
range                  T = 1..t;   // Range  of time slots.
int            length[N] = ...;    // Time slots i-th order takes.
int       min_deliver[N] = ...;    // Min slot i-th order should be delivered.
int       max_deliver[N] = ...;    // Max slot i-th order should be delivered.
float          profit[N] = ...;    // Profit if I take i-th order.
float         surface[N] = ...;    // Surface of i-th order.
float   surface_capacity = ...;    // Surface capacity.

//>>>>>>>>>>>>>>>>
// the task i starts at slot j
dvar boolean x_ij[i in N, j in T]; 
//<<<<<<<<<<<<<<<<

execute
{
	for(var i=1; i<=n; i++){
	  	var error = false;
		if (min_deliver[i]<length[i]){
			writeln ( "Warning: input data inegrity min_deliver<length for task " + i );	
			min_deliver[i] = length[i];
		}
		
		if (max_deliver[i]>t){
			writeln ( "Warning: input data inegrity max_deliver[i]>t for task " + i );	
			max_deliver[i] = t;
		}
		
		if (max_deliver[i]<min_deliver[i]){
			writeln ( "Error: input data inegrity max_deliver[i]<min_deliver[i] for task " + i );	
		}
	}	

};



//>>>>>>>>>>>>>>>>
maximize sum(i in N)(sum(j in T)x_ij[i,j] * profit[i]);  
//<<<<<<<<<<<<<<<<

subject to {


    //>>>>>>>>>>>>>>>>
    
    // a task could be executed or not
    forall(i in N)
    sum(j in T)x_ij[i,j] <= 1; 
            
    /* delivery slot constraint*/
    forall(i in N)
    sum(j in T) ( j * x_ij[i,j] ) <= (sum(j in 1..(t-length[i]+1))x_ij[i,j]) * (max_deliver[i] - length[i] + 1);
    
    forall(i in N)
    sum(j in T) ( j * x_ij[i,j] ) >= (sum(j in 1..(t-length[i]+1))x_ij[i,j]) * (min_deliver[i] - length[i] + 1);
    
    /*oven capacity - dynamic window of search*/
	forall(j in T)
    sum (i in N)
    sum (k in ((j >= length[i]) ? (j - length[i] + 1) : 1)..j) 
		x_ij[i][k] * surface[i] <= surface_capacity;
    
    //<<<<<<<<<<<<<<<<
}

//>>>>>>>>>>>>>>>>
execute
{
	write ( "                    \t");
	for(var j=1; j<=t; j++){
	  write ( ""+j+"\t");
	}
	write("\n");
	for(var i=1; i<=n; i++){
	  write ( "task_"+i+" (surface : " + surface[i]+ ")\t");
	  var processed = false;
	  	for(var j=1; j<=t; j++){
	  	  if(x_ij[i][j] == 1){
	  	    processed = true;
	  	  	for(var k=j; k<=j+length[i]-1; k++){
	  	  	  write ( "X\t");	
	  	  	}
	  	  	j = k - 1;
	  	  }else{
	  	    write ( "-\t");
	  	  }
	  	}
	  	write("\n"+ (processed ? "taken +"+profit[i] : "not taken") + "\n");
	}	

};
//<<<<<<<<<<<<<<<<
