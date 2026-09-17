public class Dog extends  Animal{
    public Dog(String name) {
        super(name);
    }

    @Override
    public void speak() {
        System.out.println(getName() + " 汪汪汪");
    }

    public static void main(String[] args) {
        Dog dog = new Dog("旺财");
        dog.speak();
    }
}
