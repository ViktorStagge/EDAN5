package assignment1;

import java.util.Random;
import helpers.Statistics;



public class MarkingTree {
	public static void main(String[] args){
		int[] int_to_test = {2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20}; 
		int n_test_each = 100;
		
		long start_time = System.currentTimeMillis(); 
		Random r = new Random();
		
		for(int height : int_to_test){
			int[] values1 = new int[n_test_each];
			int[] values2 = new int[n_test_each];
			 
			for(int i = 0; i < n_test_each; i++){
				values1[i] = simulateAlice1(height, r);
				values2[i] = simulateAlice2(height, r);
			}
			print("Height: " + height);
			print(String.format("%.1f ± %.1f", Statistics.mean(values1), Statistics.std(values1, 0)));
			print(String.format("%.1f ± %.1f", Statistics.mean(values2), Statistics.std(values2, 0)));
		}
		
		/*
		int height = 19;
		print("Steps to complete: " + simulateAlice1(height, r));
		print("Steps to complete: " + simulateAlice2(height, r));
		print("Steps to complete: " + simulateAlice3(height, r)); */
		
		print("Time taken: " + ((System.currentTimeMillis() - start_time)/1000) + "s.");
	}
	
	private static int simulateAlice1(int height, Random r){
		Tree t1 = new Tree(height);
		int N = (1 << height) - 1;
		int n_rounds = 0;
		
		while(!t1.filled()){
			t1.mark(r.nextInt(N) + 1);
			n_rounds++;
		}
		return n_rounds;
	}
	
	private static int simulateAlice2(int height, Random r){
		Tree t2 = new Tree(height);
		int N = (1 << height) - 1;
		int[] p = Statistics.randomSequence(N);
		int i = 0;
		int n_rounds = 0;
		
		while(!t2.filled()){
			t2.mark(p[i++]);
			n_rounds++;
		}
		return n_rounds;
	}
	
	private static int simulateAlice3(int height, Random r){
		Tree t3 = new Tree(height);
		int N = (1 << height) - 1;
		int[] p = Statistics.randomSequence(N);
		int i = 0;
		int n_rounds = 0;
		
		while(!t3.filled()){
			if(!t3.marked(p[i])){
				t3.mark(p[i]);
				n_rounds++;
			}
			i++;
		}
		return n_rounds;
	}
	
	public static void print(Object o){
		System.out.println(o);
	}
}
