// Known Dependencies
// -> java.lang.String

package eu.bogoe.dtu.noclasses;

public enum Country {

    DENMARK ("Denmark", "Danish", 45),
    SWEDEN  ("Sweden", "Swedish", 46),
    NORWAY  ("Norway", "Norwegian", 47);

    public String country;
    public String language;
    public int phone;

    Country(String country, String language, int phone) {
        this.country = country;
        this.language = language;
        this.phone = phone;
    }
}
