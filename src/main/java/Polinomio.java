import java.util.Scanner;

public class Polinomio {
    private final double[] coeficientes;
    private final double x;
    public Polinomio(String polinomio, double numero) {


        x = numero;

        // Dividir el polinomio en términos individuales
        String[] terminos = polinomio.split("\\s*\\+\\s*|\\s*\\-\\s*");

        // Determinar el grado máximo del polinomio
        int gradoMaximo = 0;
        for (String termino : terminos) {
            int grado = obtenerGrado(termino);
            gradoMaximo = Math.max(grado, gradoMaximo);
        }

        // Inicializar el arreglo de coeficientes
        coeficientes = new double[gradoMaximo + 1];

        // Asignar los coeficientes en el arreglo
        for (String termino : terminos) {
            double coeficiente = obtenerCoeficiente(termino);
            int grado = obtenerGrado(termino);
            coeficientes[grado] = coeficiente;
        }
    }

    public double imprimirCoeficientes() {
        double resultado = 0.;

        for (int i = 0; i < coeficientes.length; i++) {

            resultado += coeficientes[i] * Math.pow(x, i);
        }
        return resultado;
    }

    private double obtenerCoeficiente(String termino) {
        String coeficienteStr = termino.split("x")[0];
        if (coeficienteStr.isEmpty()) {
            return 1.0;
        } else if (coeficienteStr.equals("-")) {
            return -1.0;
        } else {
            return Double.parseDouble(coeficienteStr);
        }
    }

    private int obtenerGrado(String termino) {
        if (termino.contains("^")) {
            String gradoStr = termino.split("\\^")[1];
            return Integer.parseInt(gradoStr);
        } else if (termino.contains("x")) {
            return 1;
        } else {
            return 0;
        }
    }

    public static void main(String[] args) {
        double x=5;
        double dx= (double) (10-5)/200;
        double respuesta = 0;
        for(double i=5+6*dx; i < 5+12*dx;  i = i+dx ){ // 200 intervalos
            Polinomio polinomio = new Polinomio("7x^1+8x^2",i);
            respuesta += polinomio.imprimirCoeficientes();

        }

        System.out.println("La respuesta es: "+(respuesta ));

    }
}