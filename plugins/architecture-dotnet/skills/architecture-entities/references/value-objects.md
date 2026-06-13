# Value Objects

## Conceito

Value Objects são objetos definidos por seus atributos, não por uma identidade. São imutáveis e comparados por valor.

## Estrutura de Arquivos

```
Domain/
└── ValueObjects/
    ├── Money.cs
    ├── Address.cs
    ├── Email.cs
    ├── PhoneNumber.cs
    └── DateRange.cs
```

---

## Value Object Base

```csharp
// Domain/Common/ValueObject.cs
namespace Domain.Common;

public abstract class ValueObject : IEquatable<ValueObject>
{
    protected abstract IEnumerable<object?> GetEqualityComponents();
    
    public override bool Equals(object? obj)
    {
        if (obj is null || obj.GetType() != GetType())
            return false;
        
        return Equals((ValueObject)obj);
    }
    
    public bool Equals(ValueObject? other)
    {
        if (other is null)
            return false;
        
        return GetEqualityComponents()
            .SequenceEqual(other.GetEqualityComponents());
    }
    
    public override int GetHashCode()
    {
        return GetEqualityComponents()
            .Select(x => x?.GetHashCode() ?? 0)
            .Aggregate((x, y) => x ^ y);
    }
    
    public static bool operator ==(ValueObject? left, ValueObject? right)
    {
        return Equals(left, right);
    }
    
    public static bool operator !=(ValueObject? left, ValueObject? right)
    {
        return !Equals(left, right);
    }
}
```

### Alternativa: Value Object como Record

```csharp
// Records já são imutáveis e têm igualdade por valor
public record Money(decimal Amount, string Currency)
{
    // Validação no construtor
    public Money
    {
        if (Amount < 0)
            throw new ArgumentException("Valor não pode ser negativo", nameof(Amount));
        
        if (string.IsNullOrWhiteSpace(Currency) || Currency.Length != 3)
            throw new ArgumentException("Moeda deve ter 3 caracteres", nameof(Currency));
        
        Currency = Currency.ToUpperInvariant();
    }
}
```

---

## Exemplos Completos

### Money (Valor Monetário)

```csharp
// Domain/ValueObjects/Money.cs
namespace Domain.ValueObjects;

public class Money : ValueObject
{
    public decimal Amount { get; }
    public string Currency { get; }
    
    private Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency.ToUpperInvariant();
    }
    
    public static Money Create(decimal amount, string currency = "BRL")
    {
        if (amount < 0)
            throw new ArgumentException("Valor não pode ser negativo", nameof(amount));
        
        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3)
            throw new ArgumentException("Moeda inválida", nameof(currency));
        
        return new Money(Math.Round(amount, 2), currency);
    }
    
    public static Money Zero(string currency = "BRL") => new(0, currency);
    
    // Operações
    public Money Add(Money other)
    {
        EnsureSameCurrency(other);
        return new Money(Amount + other.Amount, Currency);
    }
    
    public Money Subtract(Money other)
    {
        EnsureSameCurrency(other);
        var result = Amount - other.Amount;
        
        if (result < 0)
            throw new InvalidOperationException("Resultado não pode ser negativo");
        
        return new Money(result, Currency);
    }
    
    public Money Multiply(decimal factor)
    {
        if (factor < 0)
            throw new ArgumentException("Fator não pode ser negativo", nameof(factor));
        
        return new Money(Math.Round(Amount * factor, 2), Currency);
    }
    
    public Money Multiply(int quantity)
    {
        return Multiply((decimal)quantity);
    }
    
    public bool IsZero() => Amount == 0;
    
    public bool IsGreaterThan(Money other)
    {
        EnsureSameCurrency(other);
        return Amount > other.Amount;
    }
    
    public bool IsLessThan(Money other)
    {
        EnsureSameCurrency(other);
        return Amount < other.Amount;
    }
    
    private void EnsureSameCurrency(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException(
                $"Não é possível operar moedas diferentes: {Currency} e {other.Currency}");
    }
    
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Amount;
        yield return Currency;
    }
    
    public override string ToString() => $"{Currency} {Amount:N2}";
    
    // Operadores
    public static Money operator +(Money left, Money right) => left.Add(right);
    public static Money operator -(Money left, Money right) => left.Subtract(right);
    public static Money operator *(Money money, decimal factor) => money.Multiply(factor);
    public static Money operator *(Money money, int quantity) => money.Multiply(quantity);
    public static bool operator >(Money left, Money right) => left.IsGreaterThan(right);
    public static bool operator <(Money left, Money right) => left.IsLessThan(right);
    public static bool operator >=(Money left, Money right) => !left.IsLessThan(right);
    public static bool operator <=(Money left, Money right) => !left.IsGreaterThan(right);
}
```

### Address (Endereço)

```csharp
// Domain/ValueObjects/Address.cs
namespace Domain.ValueObjects;

public class Address : ValueObject
{
    public string Street { get; }
    public string Number { get; }
    public string? Complement { get; }
    public string Neighborhood { get; }
    public string City { get; }
    public string State { get; }
    public string ZipCode { get; }
    public string Country { get; }
    
    private Address(
        string street,
        string number,
        string? complement,
        string neighborhood,
        string city,
        string state,
        string zipCode,
        string country)
    {
        Street = street;
        Number = number;
        Complement = complement;
        Neighborhood = neighborhood;
        City = city;
        State = state;
        ZipCode = zipCode;
        Country = country;
    }
    
    public static Address Create(
        string street,
        string number,
        string? complement,
        string neighborhood,
        string city,
        string state,
        string zipCode,
        string country = "Brasil")
    {
        if (string.IsNullOrWhiteSpace(street))
            throw new ArgumentException("Rua é obrigatória", nameof(street));
        
        if (string.IsNullOrWhiteSpace(number))
            throw new ArgumentException("Número é obrigatório", nameof(number));
        
        if (string.IsNullOrWhiteSpace(city))
            throw new ArgumentException("Cidade é obrigatória", nameof(city));
        
        if (string.IsNullOrWhiteSpace(state))
            throw new ArgumentException("Estado é obrigatório", nameof(state));
        
        if (string.IsNullOrWhiteSpace(zipCode))
            throw new ArgumentException("CEP é obrigatório", nameof(zipCode));
        
        // Normalizar CEP
        var normalizedZipCode = new string(zipCode.Where(char.IsDigit).ToArray());
        
        if (normalizedZipCode.Length != 8)
            throw new ArgumentException("CEP deve ter 8 dígitos", nameof(zipCode));
        
        return new Address(
            street.Trim(),
            number.Trim(),
            complement?.Trim(),
            neighborhood.Trim(),
            city.Trim(),
            state.Trim().ToUpperInvariant(),
            normalizedZipCode,
            country.Trim());
    }
    
    public string GetFormattedZipCode() => $"{ZipCode[..5]}-{ZipCode[5..]}";
    
    public string GetFullAddress()
    {
        var complement = string.IsNullOrWhiteSpace(Complement) ? "" : $", {Complement}";
        return $"{Street}, {Number}{complement} - {Neighborhood}, {City}/{State} - {GetFormattedZipCode()}";
    }
    
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Street.ToUpperInvariant();
        yield return Number.ToUpperInvariant();
        yield return Complement?.ToUpperInvariant();
        yield return Neighborhood.ToUpperInvariant();
        yield return City.ToUpperInvariant();
        yield return State;
        yield return ZipCode;
        yield return Country.ToUpperInvariant();
    }
    
    public override string ToString() => GetFullAddress();
}
```

### Email

```csharp
// Domain/ValueObjects/Email.cs
using System.Text.RegularExpressions;

namespace Domain.ValueObjects;

public partial class Email : ValueObject
{
    public string Value { get; }
    
    private Email(string value)
    {
        Value = value.ToLowerInvariant();
    }
    
    public static Email Create(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Email é obrigatório", nameof(value));
        
        value = value.Trim();
        
        if (value.Length > 256)
            throw new ArgumentException("Email deve ter no máximo 256 caracteres", nameof(value));
        
        if (!EmailRegex().IsMatch(value))
            throw new ArgumentException("Email inválido", nameof(value));
        
        return new Email(value);
    }
    
    public string GetDomain() => Value.Split('@')[1];
    
    public string GetLocalPart() => Value.Split('@')[0];
    
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Value;
    }
    
    public override string ToString() => Value;
    
    // Conversão implícita
    public static implicit operator string(Email email) => email.Value;
    
    [GeneratedRegex(@"^[^@\s]+@[^@\s]+\.[^@\s]+$", RegexOptions.IgnoreCase)]
    private static partial Regex EmailRegex();
}
```

### PhoneNumber

```csharp
// Domain/ValueObjects/PhoneNumber.cs
namespace Domain.ValueObjects;

public class PhoneNumber : ValueObject
{
    public string CountryCode { get; }
    public string AreaCode { get; }
    public string Number { get; }
    
    private PhoneNumber(string countryCode, string areaCode, string number)
    {
        CountryCode = countryCode;
        AreaCode = areaCode;
        Number = number;
    }
    
    public static PhoneNumber Create(string fullNumber)
    {
        if (string.IsNullOrWhiteSpace(fullNumber))
            throw new ArgumentException("Telefone é obrigatório", nameof(fullNumber));
        
        // Remover caracteres não numéricos
        var digits = new string(fullNumber.Where(char.IsDigit).ToArray());
        
        return digits.Length switch
        {
            // Formato: 11999999999 (Brasil sem código do país)
            10 or 11 => new PhoneNumber("55", digits[..2], digits[2..]),
            
            // Formato: 5511999999999 (Brasil com código do país)
            12 or 13 when digits.StartsWith("55") => new PhoneNumber("55", digits[2..4], digits[4..]),
            
            _ => throw new ArgumentException("Formato de telefone inválido", nameof(fullNumber))
        };
    }
    
    public static PhoneNumber Create(string countryCode, string areaCode, string number)
    {
        var cleanCountry = new string(countryCode.Where(char.IsDigit).ToArray());
        var cleanArea = new string(areaCode.Where(char.IsDigit).ToArray());
        var cleanNumber = new string(number.Where(char.IsDigit).ToArray());
        
        if (cleanArea.Length != 2)
            throw new ArgumentException("DDD deve ter 2 dígitos", nameof(areaCode));
        
        if (cleanNumber.Length < 8 || cleanNumber.Length > 9)
            throw new ArgumentException("Número deve ter 8 ou 9 dígitos", nameof(number));
        
        return new PhoneNumber(cleanCountry, cleanArea, cleanNumber);
    }
    
    public bool IsMobile() => Number.Length == 9 && Number.StartsWith("9");
    
    public string GetFormatted() => $"+{CountryCode} ({AreaCode}) {FormatNumber()}";
    
    public string GetE164() => $"+{CountryCode}{AreaCode}{Number}";
    
    private string FormatNumber()
    {
        return Number.Length == 9
            ? $"{Number[..5]}-{Number[5..]}"
            : $"{Number[..4]}-{Number[4..]}";
    }
    
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return CountryCode;
        yield return AreaCode;
        yield return Number;
    }
    
    public override string ToString() => GetFormatted();
}
```

### DateRange (Período)

```csharp
// Domain/ValueObjects/DateRange.cs
namespace Domain.ValueObjects;

public class DateRange : ValueObject
{
    public DateTime Start { get; }
    public DateTime End { get; }
    
    private DateRange(DateTime start, DateTime end)
    {
        Start = start;
        End = end;
    }
    
    public static DateRange Create(DateTime start, DateTime end)
    {
        if (end < start)
            throw new ArgumentException("Data final deve ser maior ou igual à data inicial");
        
        return new DateRange(start, end);
    }
    
    public static DateRange CreateDay(DateTime date) => 
        new(date.Date, date.Date.AddDays(1).AddTicks(-1));
    
    public static DateRange CreateMonth(int year, int month) =>
        new(new DateTime(year, month, 1), 
            new DateTime(year, month, 1).AddMonths(1).AddTicks(-1));
    
    public static DateRange CreateYear(int year) =>
        new(new DateTime(year, 1, 1), 
            new DateTime(year, 12, 31, 23, 59, 59, 999));
    
    public int TotalDays => (int)(End - Start).TotalDays + 1;
    
    public int TotalHours => (int)(End - Start).TotalHours;
    
    public bool Contains(DateTime date) => date >= Start && date <= End;
    
    public bool Overlaps(DateRange other) => 
        Start <= other.End && other.Start <= End;
    
    public bool IsAdjacent(DateRange other) =>
        End.AddTicks(1) == other.Start || other.End.AddTicks(1) == Start;
    
    public DateRange? Intersection(DateRange other)
    {
        if (!Overlaps(other))
            return null;
        
        var intersectStart = Start > other.Start ? Start : other.Start;
        var intersectEnd = End < other.End ? End : other.End;
        
        return new DateRange(intersectStart, intersectEnd);
    }
    
    public DateRange Union(DateRange other)
    {
        if (!Overlaps(other) && !IsAdjacent(other))
            throw new InvalidOperationException("Períodos não são contíguos");
        
        var unionStart = Start < other.Start ? Start : other.Start;
        var unionEnd = End > other.End ? End : other.End;
        
        return new DateRange(unionStart, unionEnd);
    }
    
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Start;
        yield return End;
    }
    
    public override string ToString() => $"{Start:dd/MM/yyyy} - {End:dd/MM/yyyy}";
}
```

---

## Configuração EF Core para Value Objects

```csharp
// Infrastructure/Persistence/Configurations/OrderConfiguration.cs
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        
        // Value Object: Money
        builder.OwnsOne(o => o.TotalAmount, money =>
        {
            money.Property(m => m.Amount)
                .HasColumnName("TotalAmount")
                .HasPrecision(18, 2);
            
            money.Property(m => m.Currency)
                .HasColumnName("Currency")
                .HasMaxLength(3);
        });
        
        // Value Object: Address
        builder.OwnsOne(o => o.ShippingAddress, address =>
        {
            address.Property(a => a.Street)
                .HasColumnName("ShippingStreet")
                .HasMaxLength(200);
            
            address.Property(a => a.Number)
                .HasColumnName("ShippingNumber")
                .HasMaxLength(20);
            
            address.Property(a => a.Complement)
                .HasColumnName("ShippingComplement")
                .HasMaxLength(100);
            
            address.Property(a => a.Neighborhood)
                .HasColumnName("ShippingNeighborhood")
                .HasMaxLength(100);
            
            address.Property(a => a.City)
                .HasColumnName("ShippingCity")
                .HasMaxLength(100);
            
            address.Property(a => a.State)
                .HasColumnName("ShippingState")
                .HasMaxLength(2);
            
            address.Property(a => a.ZipCode)
                .HasColumnName("ShippingZipCode")
                .HasMaxLength(8);
            
            address.Property(a => a.Country)
                .HasColumnName("ShippingCountry")
                .HasMaxLength(50);
        });
    }
}
```
