package model.user;

public abstract class User {

    protected String id;
    protected String name;
    protected String email;
    protected String phone;
    protected String password;

    public User(String id, String name, String email, String phone, String password) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.password = password;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getPhone() {
        return phone;
    }
    public String getPassword() {
    return password;
}
    public abstract boolean login(String password);

    public abstract void logout();

    public void updateContact(String email, String phone) {
        this.email = email;
        this.phone = phone;
    }
}