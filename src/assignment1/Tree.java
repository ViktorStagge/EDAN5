package assignment1;

public class Tree {
	private boolean[] nodes;
	private int n_marked = 0;
	
	public Tree(int height){
		nodes = new boolean[(1 << height) - 1];
	}
	
	public void mark(int n){
		if(!nodes[n-1]){
			nodes[n-1] = true;
			n_marked++;
			
			// mark children
			if(marked(2*n)){
				mark(2*n + 1);
			} else if(marked(2*n + 1)){
				mark(2*n);
			}
			
			// mark parent/sibling
			if(marked(n - n%2 + 1 - n%2)){
				mark(n/2);
			} else if(marked(n/2)){
				mark(n + 1 - n%2 - n%2);
			}
		}
	}
	
	public boolean marked(int n){
		if(n < 1 || n > nodes.length){
			return false;
		} else {
			return nodes[n-1];
		}
	}
	
	public boolean filled(){
		return n_marked == nodes.length;
	}
	
	@Override
	public String toString(){
		StringBuilder sb = new StringBuilder();
		sb.append("Tree: nodes=" + nodes.length + "\n[");
		for(boolean b : nodes){
			sb.append(b + ", ");
		}
		sb.append("]");
		return sb.toString();
	}
}
