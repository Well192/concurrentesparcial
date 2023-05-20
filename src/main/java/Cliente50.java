import java.util.Scanner;

class Cliente50 {

    public double[] sum = new double[40];
    TCPClient50 mTcpClient;
    Scanner sc;

    public static void main(String[] args) {
        Cliente50 objcli = new Cliente50();
        objcli.iniciar();
    }
    void iniciar() {
        new Thread(
                () -> {
                    mTcpClient = new TCPClient50("127.0.0.1", message -> ClienteRecibe(message));
                    mTcpClient.run();
                }
        ).start();
        //---------------------------

        String salir = "n";
        sc = new Scanner(System.in);
        System.out.println("Cliente bandera 01");
        while (!salir.equals("s")) {
            salir = sc.nextLine();
            ClienteEnvia(salir);
        }
        System.out.println("Cliente bandera 02");

    }

    void ClienteRecibe(String llego) {
        System.out.println("CLINTE50 El mensaje::" + llego);
        if (llego.trim().contains("evalua")) {
            String[] arrayString = llego.split("\\s+");
            String polinomio = arrayString[1];
            int a = Integer.parseInt(arrayString[2]);
            int b = Integer.parseInt(arrayString[3]);
            int cantidad =  Integer.parseInt(arrayString[4]);
            int rango = Integer.parseInt(arrayString[5]);
            System.out.println("El polinomio: "+polinomio+", el min:" + a + " el max:" + b+", "+cantidad);
            procesar(polinomio,a, b,cantidad, rango);
        }
    }

    void ClienteEnvia(String envia) {
        if (mTcpClient != null) {
            mTcpClient.sendMessage(envia);
        }
    }

    void procesar(String polinomio, double a, double b, int cantidad, int rango) {

        int numIntervalos = (int) (((b-a)*cantidad)/rango);

        int H = 6;//luego aumentar

        double dx = (double) (rango) / cantidad;

        int limite = numIntervalos/H;

        Thread[] todos = new Thread[40];
        for (int i = 0; i < (H - 1); i++) {

            todos[i] = new tarea0101((i * dx*limite + a), ((i * dx*limite) +( dx*limite) + a), i,dx, polinomio);
            todos[i].start();
        }

        todos[H - 1] = new tarea0101(((dx*limite * (H - 1)) + a), (b), H - 1,dx, polinomio);
        todos[H - 1].start();
        for (int i = 0; i <= (H - 1); i++) {//AQUI AQUI VER <=
            try {
                todos[i].join();
            } catch (InterruptedException ex) {
                System.out.println("error" + ex);
            }
        }
        double sumatotal = 0;
        for (int i = 0; i < H; i++) {

            sumatotal = sumatotal + sum[i];
        }
        System.out.println(sumatotal*dx);
        ClienteEnvia("rpta " + sumatotal*dx);
    }
    public class tarea0101 extends Thread {
        public double max, min;
        int id;
        double dx;

        String polinomio;
        tarea0101(double min_, double max_, int id_, double dx,String polinomio_) {
            max = max_;
            min = min_;
            id = id_;
            this.dx = dx;
            polinomio = polinomio_;
        }
        public void run() {
            double suma = 0;

            for (double i = min; i < max; i=i+dx) {
                Polinomio polinomio = new Polinomio(this.polinomio,i);
                suma += polinomio.evaluando_en_polinomio();

            }
            sum[id] = suma;
            System.out.println(" min:" + min + " max:" + (max ) + " id:" + id + " suma:" + (suma));
            // envio 7x^1+8x^2 5 10 200
        }
    }

}
